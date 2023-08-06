import networkx as nx

from virtualitics import exceptions, utils, vip_result, vip_plot
import virtualitics
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import pandas as pd
import json
import tabulate
from IPython.display import display, HTML

DEBUG_LEVEL = 2


def generic_callback(response_bytes, payload, log_level, figsize):
    """
    General callback called upon API request response

    :param response_bytes: The header of the request received
    :param payload: Larger data
    :param log_level: logging level used in the callbacks
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from VIP. The
    resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
    (8, 8).
    :return: Default None or pd.DataFrame containing column(s) of results
    """
    results = []
    response = json.loads(response_bytes.decode())
    if log_level == DEBUG_LEVEL:
        print(response)
    if (response["AuthStatus"] == "Success") and (response["VersionStatus"] == "Success"):
        if "SpecialResponse" in response:
            print(response["SpecialResponse"] + "\n")
            return None
        task_failures = []
        task_index = 1
        for task_response in response["TaskResponses"]:
            task_status = task_response.get("TaskStatus") or "Failed"
            if task_status != "Success":
                task_failures.append(task_response)
            else:
                # Handle outputs for specific task types
                output = _process_specific_task(task_response, payload, log_level, figsize)
                if output is not None:
                    results.append(output)

            task_index += 1

        if len(task_failures) > 0:
            failure = task_failures[0]
            task_type = failure.get('TaskType') or 'unknown'
            error = failure.get('Error') or '(unknown reason)'
            error = error.replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
            exception_message = "Task '%s' failed because '%s'" % (task_type, error)
            if (task_type == "unknown") and (error == "(unknown reason)"):
                raise exceptions.VipTaskUnknownExecutionException("The VIP task execution failed without providing a "
                                                                  "reason. Please try running the command again. ")
            # also print 'Note' attribute if it exists
            if "Note" in failure:
                note = failure["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip()
                exception_message += ". Note: '%s'" % note
            raise exceptions.VipTaskExecutionException(exception_message)
        if len(results) == 0:
            return None
        elif len(results) > 0:
            return vip_result.VipResult(results)
        else:
            raise (exceptions.MultipleObjectsToReturnException("There was more than one object to return to caller!"))
    else:
        # Priority given to authentication errors
        if response["AuthStatus"] != "Success":
            # Raise and exception with the bubbled up error message from VIP
            raise exceptions.AuthenticationException(response["Error"])
        if response["VersionStatus"] != "Success":
            if response["VersionStatusFailReason"] == "InvalidApiVersion":
                raise exceptions.VersionMismatchException(
                    "pyVIP version (" + virtualitics.__version__ + ") is not supported by the installed version " +
                    "of VIP (" + response["VIPVersion"] + "). VIP expecting pyVIP version (" +
                    response["ExpectedAPIVersion"] + ") or greater. Check 'Version' section in the documentation " +
                    "and update the appropriate tool.")
            elif response["VersionStatusFailReason"] == "InvalidVIPVersion":
                raise exceptions.VersionMismatchException(
                    "VIP version (" + response["VIPVersion"] + ") is not supported by the installed version of " +
                    "pyVIP (" + virtualitics.__version__ + "). pyVIP expecting VIP version (" +
                    virtualitics.__latest_compatible_vip_version__ + ") or greater. Check 'Version' section in the " +
                    "documentation and update the appropriate tool.")


def _process_specific_task(task_response, payload, log_level, figsize):
    """
    Processes the responses for specific task types. When adding a specific callback create the function and then add
    the task type and function name to the switcher dictionary

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :param log_level: logging level used in the callbacks
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from VIP. The
    resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
    (8, 8).
    :return: Output of any specific task processing
    """
    # Maps task types to callback functions
    task_type = task_response["TaskType"]
    if task_type == "Export":
        return _export_callback(task_response, payload, figsize)
    elif task_type == "SmartMapping":
        return _smart_mapping_callback(task_response, payload)
    elif task_type == "AnomalyDetection" or task_type == "PcaAnomalyDetection":
        return _ad_callback(task_response, payload)
    elif task_type == "Pca":
        return _pca_callback(task_response, payload)
    elif task_type == "Clustering":
        return _clustering_callback(task_response, payload)
    elif task_type == "PlotMappingExport":
        return _plot_mapping_export_callback(task_response, payload, log_level)
    elif task_type == "VisiblePoints":
        return _ml_routine_callback(task_response, payload)
    elif task_type == "HeatmapFeature":
        return _ml_routine_callback(task_response, payload)
    elif task_type == "AddRows":
        return _ml_routine_callback(task_response, payload)
    elif task_type == "Filter":
        return _filter_callback(task_response, payload)
    elif task_type == "ColumnSync":
        return _column_sync_callback(task_response, payload)
    elif task_type == "ConvertColumn":
        return _convert_column_callback(task_response, payload)
    elif task_type == "GetNetwork":
        return _get_network_callback(task_response, payload)
    elif task_type == "PageRank":
        return _pagerank_callback(task_response, payload)
    elif task_type == "ClusteringCoefficient":
        return _clustering_coefficient_callback(task_response, payload)
    elif task_type == "GraphDistance":
        return _graph_distance_callback(task_response, payload)
    elif task_type == "Structure":
        return _structure_callback(task_response, payload)
    elif task_type == "Insights":
        return _insights_callback(task_response, payload)
    return None


def _plot_mapping_export_callback(task_response, payload, log_level):
    """
    Callback handler for plot mapping export tasks

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array. unused here
    :param log_level: logging level used in the callbacks to set in returned vip plot
    :return: :class:`VipPlot` object instance
    """
    if not task_response["ReturnPlotMapping"]:
        return None

    plot = vip_plot.VipPlot(data_set_name=task_response["DataSetName"], plot_type=task_response["PlotType"],
                            map_mode=task_response["MapMode"], name=task_response["PlotName"], log_level=log_level)

    if "X" in task_response.keys() and task_response["X"] is not None:
        plot.x = task_response["X"]
    if "Y" in task_response.keys() and task_response["Y"] is not None:
        plot.y = task_response["Y"]
    if "Z" in task_response.keys() and task_response["Z"] is not None:
        plot.z = task_response["Z"]
    if "Color" in task_response.keys() and task_response["Color"] is not None:
        plot.color = task_response["Color"]
    if "Size" in task_response.keys() and task_response["Size"] is not None:
        plot.size = task_response["Size"]
    if "Shape" in task_response.keys() and task_response["Shape"] is not None:
        plot.shape = task_response["Shape"]
    if "Groupby" in task_response.keys() and task_response["Groupby"] is not None:
        plot.groupby = task_response["Groupby"]
    if "Playback" in task_response.keys() and task_response["Playback"] is not None:
        plot.playback = task_response["Playback"]
    if "Transparency" in task_response.keys() and task_response["Transparency"] is not None:
        plot.transparency = task_response["Transparency"]
    if "Halo" in task_response.keys() and task_response["Halo"] is not None:
        plot.halo = task_response["Halo"]
    if "Pulsation" in task_response.keys() and task_response["Pulsation"] is not None:
        plot.pulsation = task_response["Pulsation"]
    if "Arrow" in task_response.keys() and task_response["Arrow"] is not None:
        plot.arrow = task_response["Arrow"]
    if "XScale" in task_response.keys() and task_response["XScale"] is not None:
        plot.x_scale = task_response["XScale"]
    if "YScale" in task_response.keys() and task_response["YScale"] is not None:
        plot.y_scale = task_response["YScale"]
    if "ZScale" in task_response.keys() and task_response["ZScale"] is not None:
        plot.z_scale = task_response["ZScale"]
    if "SizeScale" in task_response.keys() and task_response["SizeScale"] is not None:
        plot.size_scale = task_response["SizeScale"]
    if "TransparencyScale" in task_response.keys() and task_response["TransparencyScale"] is not None:
        plot.transparency_scale = task_response["TransparencyScale"]
    if "HaloScale" in task_response.keys() and task_response["HaloScale"] is not None:
        plot.halo_scale = task_response["HaloScale"]
    if "ArrowScale" in task_response.keys() and task_response["ArrowScale"] is not None:
        plot.arrow_scale = task_response["ArrowScale"]
    if "ColorType" in task_response.keys() and task_response["ColorType"] is not None:
        plot.color_type = task_response["ColorType"]
    if "ColorBins" in task_response.keys() and task_response["ColorBins"] is not None:
        plot.color_bins = task_response["ColorBins"]
    if "ColorBinDist" in task_response.keys() and task_response["ColorBinDist"] is not None:
        plot.color_bin_dist = task_response["ColorBinDist"]
    if "ColorInverted" in task_response.keys() and task_response["ColorInverted"] is not None:
        plot.color_inverted = task_response["ColorInverted"]
    if "XNormalization" in task_response.keys() and task_response["XNormalization"] is not None:
        plot.x_normalization = task_response["XNormalization"]
    if "YNormalization" in task_response.keys() and task_response["YNormalization"] is not None:
        plot.y_normalization = task_response["YNormalization"]
    if "ZNormalization" in task_response.keys() and task_response["ZNormalization"] is not None:
        plot.z_normalization = task_response["ZNormalization"]
    if "ColorNormalization" in task_response.keys() and task_response["ColorNormalization"] is not None:
        plot.color_normalization = task_response["ColorNormalization"]
    if "SizeNormalization" in task_response.keys() and task_response["SizeNormalization"] is not None:
        plot.size_normalization = task_response["SizeNormalization"]
    if "TransparencyNormalization" in task_response.keys() and task_response["TransparencyNormalization"] is not None:
        plot.transparency_normalization = task_response["TransparencyNormalization"]
    if "ArrowNormalization" in task_response.keys() and task_response["ArrowNormalization"] is not None:
        plot.arrow_normalization = task_response["ArrowNormalization"]
    if "GlobeStyle" in task_response.keys() and task_response["GlobeStyle"] is not None:
        plot.globe_style = task_response["GlobeStyle"]
    if "LatLongLines" in task_response.keys() and task_response["LatLongLines"] is not None:
        plot.lat_long_lines = task_response["LatLongLines"]
    if "CountryLines" in task_response.keys() and task_response["CountryLines"] is not None:
        plot.country_lines = task_response["CountryLines"]
    if "CountryLabels" in task_response.keys() and task_response["CountryLabels"] is not None:
        plot.country_labels = task_response["CountryLabels"]
    if "MapProvider" in task_response.keys() and task_response["MapProvider"] is not None:
        plot.map_provider = task_response["MapProvider"]
    if "MapStyle" in task_response.keys() and task_response["MapStyle"] is not None:
        plot.map_style = task_response["MapStyle"]
    if "HeatmapEnabled" in task_response.keys() and task_response["HeatmapEnabled"] is not None:
        plot.heatmap_enabled = task_response["HeatmapEnabled"]
    if "HeatmapIntensity" in task_response.keys() and task_response["HeatmapIntensity"] is not None:
        plot.heatmap_intesity = task_response["HeatmapIntensity"]
    if "HeatmapRadius" in task_response.keys() and task_response["HeatmapRadius"] is not None:
        plot.heatmap_radius = task_response["HeatmapRadius"]
    if "HeatmapRadiusUnit" in task_response.keys() and task_response["HeatmapRadiusUnit"] is not None:
        plot.heatmap_radius_unit = task_response["HeatmapRadiusUnit"]
    if "XBins" in task_response.keys() and task_response["XBins"] is not None:
        plot.x_bins = task_response["XBins"]
    if "YBins" in task_response.keys() and task_response["YBins"] is not None:
        plot.y_bins = task_response["YBins"]
    if "ZBins" in task_response.keys() and task_response["ZBins"] is not None:
        plot.z_bins = task_response["ZBins"]
    if "VolumeBy" in task_response.keys() and task_response["VolumeBy"] is not None:
        plot.hist_volume_by = task_response["VolumeBy"]
    if "SurfaceViewMode" in task_response.keys() and task_response["SurfaceViewMode"] is not None:
        plot.show_points = task_response["SurfaceViewMode"]
    if "ConfidenceLevel" in task_response.keys() and task_response["ConfidenceLevel"] is not None:
        plot.confidence = task_response["ConfidenceLevel"]

    return plot


def _export_callback(task_response, payload, figsize):
    """
    Callback handler for export tasks.

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from VIP. The
    resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
    (8, 8).
    :return: :class:`None`; displays the returned capture.
    """
    if "PayloadType" in task_response.keys():
        if task_response["PayloadType"] == "Image":
            start = task_response["BytesStartIndex"]
            size = task_response["BytesSize"]
            image_bytes = utils.decompress(utils.get_bytes(payload, start, size))
            image = Image.open(BytesIO(image_bytes))
            image = image.convert("RGB")
            matplotlib.rcParams["figure.figsize"] = figsize
            matplotlib.rcParams["figure.dpi"] = 250
            plt.imshow(np.asarray(image))
            plt.axis("off")

            if "Path" in task_response.keys():
                image.save(task_response["Path"], quality=100)

        return None


def _smart_mapping_callback(task_response, payload):
    """
    Handles the VIP response for SmartMapping

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array. not used for smart mapping
    :return: if the user opted to return_data, then returns the pd.DataFrame of the ranked features and correlation
    groups.
    """
    if "Note" in task_response:
        print("Note: '%s'\n" % task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip())
    if "ReturnData" in task_response.keys():
        if task_response["ReturnData"]:
            results = task_response["SmartMappingResults"]
            results = pd.DataFrame(results, columns=["SmartMapping Rank", "Feature", "Correlated Group"])
            results["Correlated Group"] = results["Correlated Group"].replace(-1, "None")
            if task_response["Disp"]:
                display(results[:min(5, len(results))])
                return None
            else:
                return results
        else:
            return None
    else:
        return None


def _convert_column_callback(task_response, payload):
    """
    Handles the VIP response for Filtering

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _filter_callback(task_response, payload):
    """
    Handles the VIP response for Filtering

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _column_sync_callback(task_response, payload):
    """
    Handles the VIP response for ColumnSync tasks

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _clustering_callback(task_response, payload):
    """
    Handles the VIP response for Clustering

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: :class:`None`
    """
    return _ml_routine_callback(task_response, payload)


def _ad_callback(task_response, payload):
    """
    Handles the VIP response for anomaly detection callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    """
    return _ml_routine_callback(task_response, payload)


def _pca_callback(task_response, payload):
    """
    Handled the VIP response for pca detection callback

    :param task_response: json object of the task response
    :param payload:  reference to the entire payload byte array.
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _pagerank_callback(task_response, payload):
    """
    Handles the VIP response for the pagerank callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _clustering_coefficient_callback(task_response, payload):
    """
    Handles the VIP response for the clustering coefficient callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _graph_distance_callback(task_response, payload):
    """
    Handles the VIP response for the graph distance callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _structure_callback(task_response, payload):
    """
    Handles the VIP response for the clustering coefficient callback

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array
    :return: if the user opted to return_data, then returns the pd.DataFrame of the components
    """
    return _ml_routine_callback(task_response, payload)


def _insights_callback(task_response, payload):
    table = []
    if "InsightsReport" in task_response:
        for insight in task_response["InsightsReport"]:
            table.append([insight["Title"], insight["Story"]])
        # TODO: Aakash, I don't think this works. Is vip.insights() supposed to show anything? It doesn't
        display(HTML(tabulate.tabulate(table, headers=["Topic", "Insight"], tablefmt='html')))


def _ml_routine_callback(task_response, payload):
    """
    Generic handler for ML routines.

    :param task_response: json object of the task response
    :param payload: reference to the entire payload byte array.
    :return: if the user opted to return_data, then returns the :class:`pd.DataFrame` of results
    """
    if "Note" in task_response:
        print("Note: '%s'\n" % task_response["Note"].replace('\n', '').replace('<b>', '').replace('</b>', '').strip())
    if "ReturnData" in task_response.keys():
        if task_response["ReturnData"]:
            start = task_response["BytesStartIndex"]
            size = task_response["BytesSize"]
            columns_bytes = utils.get_bytes(payload, start, size)
            columns = {}
            for col in task_response["ColumnInfo"]:
                col_bytes = utils.get_bytes(columns_bytes, col["BytesStartIndex"], col["BytesSize"])
                column = pd.Series(data=utils.deserialize_column(col["ColumnType"], col_bytes),
                                   name=col["ColumnName"])
                column.replace('', np.NaN, inplace=True)  # if value is empty string, convert to NaN
                if col["ColumnType"] == "date":
                    try:
                        column = pd.to_datetime(column)
                    except ValueError:
                        # keep as strings if the column can't be parsed into datetime format
                        pass
                columns[col["ColumnName"]] = column
            components = pd.DataFrame(data=columns)
            return components
        else:
            return None
    else:
        return None


def _get_network_callback(task_response, payload):
    if "NetworkDataFormat" in task_response.keys():
        start = task_response["BytesStartIndex"]
        size = task_response["BytesSize"]
        data_bytes = utils.get_bytes(payload, start, size)
        if task_response["NetworkDataFormat"] == "JSON":
            data = json.loads(utils.decompress(data_bytes).decode())
            g = nx.Graph()
            for node_data in data["Nodes"]:
                g.add_node(node_data["Name"], **node_data)
            for edge_data in data["Edges"]:
                g.add_edge(edge_data["Source"], edge_data["Target"], weight=edge_data["Weight"])
            return g
        elif task_response["NetworkDataFormat"] == "Edgelist":
            return _ml_routine_callback(task_response, payload)
    else:
        raise exceptions.VipTaskUnknownExecutionException("Failed to get network data from VIP. ")
