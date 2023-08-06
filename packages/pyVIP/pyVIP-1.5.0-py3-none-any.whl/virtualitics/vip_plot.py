from virtualitics import utils
from virtualitics import exceptions
from virtualitics import api


class VipPlot:
    """
    The plot class contains all essential details of a plot in VIP.
    """

    def __init__(self, data_set_name=None, plot_type="scatter", x=None, y=None, z=None, color=None, size=None,
                 shape=None, transparency=None, halo=None, halo_highlight=None, pulsation=None,
                 pulsation_highlight=None, playback=None, playback_highlight=None, arrow=None, groupby=None,
                 x_scale=None, y_scale=None, z_scale=None, size_scale=None, transparency_scale=None, halo_scale=None,
                 arrow_scale=None, color_type=None, color_normalization=None, x_normalization=None,
                 y_normalization=None, z_normalization=None, size_normalization=None, transparency_normalization=None,
                 arrow_normalization=None, show_points=None, confidence=None, map_mode=None, globe_style=None,
                 lat_long_lines=None, country_lines=None, country_labels=None, heatmap_enabled=None,
                 heatmap_intensity=None, heatmap_radius=None, heatmap_radius_unit=None, map_provider=None,
                 map_style=None, color_bins=None, color_bin_dist=None, hist_volume_by=None, viewby=None, x_bins=None,
                 y_bins=None, z_bins=None, color_inverted=None, log_level=0, name=None, _dataset_type=None):
        """
        Constructor for VipPlot instance. See parameter details.

        :param data_set_name: Name of the dataset to use when creating the plot. default: None implies use the
            currently loaded dataset.
        :param plot_type: Controls the plot type in VIP. Default is scatter.
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the column mapped to the X
            dimension is numeric. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y. This can only be set if the column mapped to the Y
            dimension is numeric. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the column mapped to the Z
            dimension is numeric. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the column mapped to the
            size dimension is numeric. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency. This can only be set if the column
            mapped to the transparency dimension is numeric. The options are "Log10", "Softmax", "IHST"
        :param lat_long_lines: :class:`bool` visibility setting for Latitude/Longitude lines.
        :param country_lines: :class:`bool` visibility setting for country border lines.
        :param country_labels: :class:`bool` visibility setting for country labels.
        :param globe_style: {"natural", "dark", "black ocean", "blue ocean", "gray ocean", "water color",
            "topographic", "moon", "night"}
        :param map_provider: {"ArcGIS", "Stamen", "OpenStreetMap"}
        :param map_style: depends on the map_provider. See documentation for options.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range}
        :param hist_volume_by: setting for metric used for size of histogram bins; {"count", "avg", "sum"}
        :param x_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'x' dimension
        :param y_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'y' dimension
        :param z_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'z' dimension
        :param color_inverted: :class:`bool` specifying whether to invert the color wheel
        :param heatmap_enabled: :class:`bool` setting for whether to use heatmap of the mapped data.
        :param heatmap_intensity: :class:`float` to determine the intensity of the heatmap. heatmap_enabled must be True
            for this parameter to be used.
        :param heatmap_radius: :class:`float` determining the radius of sensitivity for heatmap functionality.
            heatmap_enabled must be True for this parameter to be used.
        :param heatmap_radius_unit: determines the units of the heatmap_radius. Must be a :class:`str` and one of
            {"Kilometers", "Miles", "NauticalMiles"}. heatmap_enabled must be True for this parameter to be used.
        :param log_level: :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
            guide the user of important internal events. Debug level will print messages that expose a greater level of
            the internal state, useful for development and debugging purposes. Each level will print what is also
            printed at lower levels.
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :param _dataset_type: :class:`str` specifying the type of data ("tabular" or "network") for the given plot type.
            Users should not manually change this manually.
        """
        self.log_level = log_level

        # DataSet and PlotType
        self.data_set_name = data_set_name
        self._dataset_type = _dataset_type
        self._plot_type = utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, plot_type, "plot_type")

        if map_mode not in ["NONE", None]:
            if map_mode == "FLAT":
                self.plot_type(utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, "MAPS2D", "plot_type"))
            if map_mode == "GLOBE":
                self.plot_type(utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, "MAPS3D", "plot_type"))

        self.name = name

        # Plot Dimensions

        # Spatial Dimensions
        self.x = x
        self.y = y
        self.z = z

        # Appearance Dimensions
        self.color = color
        self.size = size
        self.shape = shape

        # Refine Dimensions
        self.groupby = groupby
        self.playback = playback

        # Extra Dimensions
        self.transparency = transparency
        self.halo = halo
        self.pulsation = pulsation
        self.arrow = arrow

        # Plot Settings

        # Line plots
        self.viewby = viewby

        # Scaling
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.z_scale = z_scale
        self.size_scale = size_scale
        self.transparency_scale = transparency_scale
        self.halo_scale = halo_scale
        self.arrow_scale = arrow_scale

        # Color Type
        self.color_type = color_type
        self.color_bins = color_bins
        self.color_bin_dist = color_bin_dist
        self.color_inverted = color_inverted

        # Normalization
        self.x_normalization = x_normalization
        self.y_normalization = y_normalization
        self.z_normalization = z_normalization
        self.color_normalization = color_normalization
        self.size_normalization = size_normalization
        self.transparency_normalization = transparency_normalization
        self.arrow_normalization = arrow_normalization

        # Plot type specific

        # Surfaces
        self.show_points = show_points
        self.confidence = confidence  # This is specific to confidence ellipsoid

        # Geospatial 2D Maps
        self.map_provider = map_provider
        self.map_style = map_style

        # Geospatial 3D Maps
        self.globe_style = globe_style
        self.lat_long_lines = lat_long_lines
        self.country_lines = country_lines
        self.country_labels = country_labels

        # Heatmaps
        self.heatmap_enabled = heatmap_enabled
        self.heatmap_intensity = heatmap_intensity
        self.heatmap_radius = heatmap_radius
        self.heatmap_radius_unit = heatmap_radius_unit

        # Histograms
        self.x_bins = x_bins
        self.y_bins = y_bins
        self.z_bins = z_bins
        self.hist_volume_by = hist_volume_by

        # Highlights
        self.halo_highlight = halo_highlight
        self.pulsation_highlight = pulsation_highlight
        self.playback_highlight = playback_highlight

    def __str__(self):
        buf = ""
        buf += "#######################################\n"
        buf += "Dataset: {}\n".format(self.data_set_name)
        buf += "Plot Name: {}\n".format(self.name)
        buf += "# Plot Type: {}\n".format(self._plot_type)

        # Mapped Dimensions
        buf += "# Mapped Dimensions: \n"
        if self.x is not None:
            buf += "X:\t\t{}\n".format(str(self.x))
        if self.y is not None:
            buf += "Y:\t\t{}\n".format(str(self.y))
        if self.z is not None:
            buf += "Z:\t\t{}\n".format(str(self.z))
        if self.color is not None:
            buf += "Color:\t\t{}\n".format(str(self.color))
        if self.size is not None:
            buf += "Size:\t\t{}\n".format(str(self.size))
        if self.shape is not None:
            buf += "Shape:\t\t{}\n".format(str(self.shape))
        if self.groupby is not None:
            buf += "Groupby:\t\t{}\n".format(str(self.groupby))
        if self.playback is not None:
            buf += "Playback:\t\t{}\n".format(str(self.playback))
        if self.transparency is not None:
            buf += "Transparency:\t\t{}\n".format(str(self.transparency))
        if self.halo is not None:
            buf += "Halo:\t\t{}\n".format(str(self.halo))
        if self.pulsation is not None:
            buf += "Pulsation:\t\t{}\n".format(str(self.pulsation))
        if self.arrow is not None:
            buf += "Arrow:\t\t{}\n".format(str(self.arrow))

        # Plot Settings
        buf += "# Plot Settings: \n"
        if self.x_scale is not None:
            buf += "X Scale:\t\t{}\n".format(str(self.x_scale))
        if self.y_scale is not None:
            buf += "Y Scale:\t\t{}\n".format(str(self.y_scale))
        if self.z_scale is not None:
            buf += "Z Scale:\t\t{}\n".format(str(self.z_scale))
        if self.size_scale is not None:
            buf += "Size Scale:\t\t{}\n".format(str(self.size_scale))
        if self.transparency_scale is not None:
            buf += "Transparency Scale:\t{}\n".format(str(self.transparency_scale))
        if self.halo_scale is not None:
            buf += "Halo Scale:\t\t{}\n".format(str(self.halo_scale))
        if self.arrow_scale is not None:
            buf += "Arrow Scale:\t\t{}\n".format(str(self.arrow_scale))
        if self.color_type is not None:
            buf += "ColorType:\t\t{}\n".format(str(self.color_type))
        if self.color_bins is not None:
            buf += "Color Bin Count:\t{}\n".format(str(self.color_bins))
        if self.color_bin_dist is not None:
            buf += "Color Bin Dist:\t{}\n".format(str(self.color_bin_dist))
        if self.color_inverted is not None:
            buf += "Color Inverted:\t{}\n".format(str(self.color_inverted))
        if self.x_normalization is not None:
            buf += "X Normalization:\t\t{}\n".format(str(self.x_normalization))
        if self.y_normalization is not None:
            buf += "Y Normalization:\t\t{}\n".format(str(self.y_normalization))
        if self.z_normalization is not None:
            buf += "Z Normalization:\t\t{}\n".format(str(self.z_normalization))
        if self.color_normalization is not None:
            buf += "Color Normalization:\t\t{}\n".format(str(self.color_normalization))
        if self.size_normalization is not None:
            buf += "Size Normalization:\t\t{}\n".format(str(self.size_normalization))
        if self.transparency_normalization is not None:
            buf += "Transparency Normalization:\t\t{}\n".format(str(self.transparency_normalization))
        if self.arrow_normalization is not None:
            buf += "Arrow Normalization:\t\t{}\n".format(str(self.arrow_normalization))
        if self.globe_style is not None:
            buf += "Globe Style:\t\t{}\n".format(str(self.globe_style))
        if self.lat_long_lines is not None:
            buf += "Latitude/Longitude Lines:\t\t{}\n".format(str(self.lat_long_lines))
        if self.country_labels is not None:
            buf += "Country Labels\t\t{}\n".format(str(self.country_labels))
        if self.country_lines is not None:
            buf += "Country Lines\t\t{}\n".format(str(self.country_lines))
        if self.map_provider is not None:
            buf += "Map Provider:\t\t{}\n".format(str(self.map_provider))
        if self.map_style is not None:
            buf += "Map Style:\t\t{}\n".format(str(self.map_style))
        if self.heatmap_enabled is not None:
            buf += "Heatmap Enabled:\t\t{}\n".format(str(self.heatmap_enabled))
        if self.heatmap_intensity is not None:
            buf += "Heatmap Intensity:\t\t{}\n".format(str(self.heatmap_intensity))
        if self.heatmap_radius is not None:
            buf += "Heatmap Radius:\t\t{}\n".format(str(self.heatmap_radius))
        if self.heatmap_radius_unit is not None:
            buf += "Heatmap Radius:\t\t{}\n".format(str(self.heatmap_radius_unit))
        if self.x_bins is not None:
            buf += "X Bins:\t\t{}\n".format(str(self.x_bins))
        if self.y_bins is not None:
            buf += "Y Bins:\t\t{}\n".format(str(self.y_bins))
        if self.z_bins is not None:
            buf += "Z Bins:\t\t{}\n".format(str(self.z_bins))
        if self.hist_volume_by is not None:
            buf += "Histogram Volume By:\t\t{}\n".format(str(self.hist_volume_by))
        if self.viewby is not None:
            buf += "View By:\t\t{}\n".format(str(self.viewby))
        if self.show_points is not None:
            buf += "Show Points:\t\t{}\n".format(str(self.show_points))
        if self.confidence is not None:
            buf += "Confidence Level:\t\t{}\n".format(str(self.confidence))
        buf += "#######################################\n"
        return buf

    # region Parameterization
    def _validate_plot(self):
        """
        Runs through a set of checks to validate the VipPlot object is valid.

        :return: :class:`None`
        """
        if self._plot_type == "SURFACE":
            if (self.x is None) or (self.y is None) or (self.z is None):
                raise exceptions.InvalidUsageException(
                    "Surface plots require that 'x', 'y', 'z' dimensions to be mapped. ")

        if self._plot_type == "MAPS3D" or self._plot_type == "MAPS2D":
            if (self.x is None) or (self.y is None):
                raise exceptions.InvalidUsageException(
                    "Geospatial plots require that 'x' and 'y' dimensions to be mapped "
                    "to Longitude and Latitude features, respectively. ")

        return

    def get_params(self):
        """
        Prepares a dictionary that contains the plot dimensions and all settings to be sent over in an API request.

        :return: :class:`dict`
        """
        # Before passing back the parameters. Lets just validate that this plot has what it needs to be generated.
        self._validate_plot()

        params = {"TaskType": "Plot", "PlotType": self._plot_type, "PlotName": self.name,
                  "DimensionInfo": self._get_dim_info()}

        settings = self._get_plot_settings_info()

        if len(settings.keys()) > 0:
            params["PlotSettings"] = settings

        return params

    def _get_dim_info(self):
        """
        Prepares the dimension info to be included in the parameters to send over API.

        :return: :class:`list`
        """
        dim_info = []
        if self.x is not None:
            dim_info.append({"Dimension": "X", "Column": self.x})
        if self.y is not None:
            dim_info.append({"Dimension": "Y", "Column": self.y})
        if self.z is not None:
            dim_info.append({"Dimension": "Z", "Column": self.z})
        if self.color is not None:
            dim_info.append({"Dimension": "Color", "Column": self.color})
        if self.size is not None:
            dim_info.append({"Dimension": "Size", "Column": self.size})
        if self.shape is not None:
            dim_info.append({"Dimension": "Shape", "Column": self.shape})
        if self.transparency is not None:
            dim_info.append({"Dimension": "Transparency", "Column": self.transparency})
        if self.halo is not None:
            dim_info.append({"Dimension": "Halo", "Column": self.halo})
        if self.pulsation is not None:
            dim_info.append({"Dimension": "Pulsation", "Column": self.pulsation})
        if self.playback is not None:
            dim_info.append({"Dimension": "ShowBy", "Column": self.playback})
        if self.arrow is not None:
            dim_info.append({"Dimension": "VectorField", "Column": self.arrow})
        if self.groupby is not None:
            dim_info.append({"Dimension": "GroupBy", "Column": self.groupby})
        if len(dim_info) == 0:
            raise exceptions.NothingToPlotException("Please map a feature to a dimension; use a spatial dimension "
                                                    "(x, y, z) before using the other dimensions.")
        return dim_info

    def _get_plot_settings_info(self):
        """
        Prepared the plot settings info to be included in the parameters to send over API.

        :return: :class:`dict`
        """
        settings = {}
        if self.x_scale is not None:
            settings["XScale"] = self.x_scale
        if self.y_scale is not None:
            settings["YScale"] = self.y_scale
        if self.z_scale is not None:
            settings["ZScale"] = self.z_scale
        if self.size_scale is not None:
            settings["SizeScale"] = self.size_scale
        if self.transparency_scale is not None:
            settings["TransparencyScale"] = self.transparency_scale
        if self.halo_scale is not None:
            settings["HaloScale"] = self.halo_scale
        if self.arrow_scale is not None:
            settings["ArrowScale"] = self.arrow_scale
        if self.color_type is not None:
            settings["ColorType"] = self.color_type
        if self.color_normalization is not None:
            settings["ColorNormalization"] = self.color_normalization
        if self.color_inverted is not None:
            settings["ColorInverted"] = self.color_inverted
        if self.x_normalization is not None:
            settings["XNormalization"] = self.x_normalization
        if self.y_normalization is not None:
            settings["YNormalization"] = self.y_normalization
        if self.z_normalization is not None:
            settings["ZNormalization"] = self.z_normalization
        if self.size_normalization is not None:
            settings["SizeNormalization"] = self.size_normalization
        if self.transparency_normalization is not None:
            settings["TransparencyNormalization"] = self.transparency_normalization
        if self.arrow_normalization is not None:
            settings["ArrowNormalization"] = self.arrow_normalization
        if self.show_points is not None:
            settings["SurfaceViewMode"] = self.show_points
        if self.confidence is not None:
            settings["ConfidenceLevel"] = self.confidence
        if self.lat_long_lines is not None:
            settings["LatLongLines"] = self.lat_long_lines
        if self.globe_style is not None:
            settings["GlobeStyle"] = self.globe_style
        if self.country_labels is not None:
            settings["CountryLabels"] = self.country_labels
        if self.country_lines is not None:
            settings["CountryLines"] = self.country_lines
        if self.heatmap_enabled is not None:
            settings["HeatmapEnabled"] = self.heatmap_enabled
        if self.heatmap_intensity is not None:
            settings["HeatmapIntensity"] = self.heatmap_intensity
        if self.heatmap_radius is not None:
            settings["HeatmapRadius"] = self.heatmap_radius
        if self.heatmap_radius_unit is not None:
            settings["HeatmapRadiusUnit"] = self.heatmap_radius_unit
        if self.map_provider is not None:
            settings["MapProvider"] = self.map_provider
        if self.map_style is not None:
            settings["MapStyle"] = self.map_style
        if self.color_bins is not None:
            settings["ColorBins"] = self.color_bins
        if self.color_bin_dist is not None:
            settings["ColorBinDist"] = self.color_bin_dist
        if self.hist_volume_by is not None:
            settings["VolumeBy"] = self.hist_volume_by
        if self.viewby is not None:
            settings["ViewBy"] = self.viewby
        if self.x_bins is not None:
            settings['XBins'] = self.x_bins
        if self.y_bins is not None:
            settings['YBins'] = self.y_bins
        if self.z_bins is not None:
            settings['ZBins'] = self.z_bins
        if self.halo_highlight is not None:
            settings['HaloHighlight'] = self.halo_highlight
        if self.pulsation_highlight is not None:
            settings['PulsationHighlight'] = self.pulsation_highlight
        if self.playback_highlight is not None:
            settings['PlaybackHighlight'] = self.playback_highlight

        return settings

    # endregion Parameterization

    def is_spatial_dimension_used(self):
        """
        Checks if any of the 'x', 'y', or 'z' properties are not None. This is used before attempting to map
        appearance, refinement, or extra dimensions.

        :return: :class:`bool`
        """
        spatial_dimension_used = (self.x is not None) or (self.y is not None) or (self.z is not None)
        return spatial_dimension_used

    def is_geospatial_plot(self):
        """
        Checks if the current plot type is a geospatial plot type. This is used when determining whether certain
        plot settings are applicable.

        :return: :class:`bool`
        """
        if self._plot_type in ["MAPS2D", "MAPS3D"]:
            return True
        else:
            return False

    def map_provider_style(self, provider=None, style=None):
        """
        :param provider: Map provider setting. Must be set to :class:`str` and match with one of {“ArcGIS”, “Stamen”,
            “OpenStreetMap”} or `None`, which is the default and sets VIP to use the default map provider for
            relevant plots. Map provider is only applicable when plot type is set to ‘MAPS2D’.
        :param style: Map style settings. Must be set to :class:`str` and match one of the following depending on
            the map provider: ArcGIS: {“Topographic”, “Ocean”, “Imagery”, “Gray”}, OpenStreetMap: {“Mapnik”}, Stamen:
            {“Dark”, “Light”, “Watercolor”, “Terrain”}. Map style is only applicable when plot_type is set to ‘MAPS2D’.
            The default is None which implies VIP will use the default map style for the currently set map provider.
        :return: :class:`None`

        """
        self.map_provider = provider
        self.map_style = style

    def get_best_export_view(self):
        """
        Determines if there is only one good view of the plot that will be generated.

        :return: :class:`str` if there is a better view or :class:`None` otherwise.
        """
        # get a count of the mapped spatial dimensions
        dim_count = int(self.x is not None) + int(self.y is not None) + int(self.z is not None)

        # if 3D plot, just return `None`
        if dim_count == 3:
            # allow the user to use whatever view they requested.
            return None

        elif dim_count == 2:
            # Surface plot is not applicable for this case.

            # MAPS2D should always use front view
            if self._plot_type == "MAPS2D":
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "front", "export")

            # MAPS3D only needs two dimensions to make a 3D plot
            if self._plot_type == "MAPS3D":
                return None

            # Histograms look best from perspective when there are only 2 mapped spatial dimensions
            if self._plot_type == "HISTOGRAM":
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "perspective", "export")

            # For each of these cases, the following views are optimal and look better than "ortho"
            # XY case
            if (self.x is not None) and (self.y is not None):
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "front", "export")
            # XZ case
            elif (self.x is not None) and (self.z is not None):
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "top", "export")
            # YZ case
            else:
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "right", "export")

        else:
            # Surface, MAPS2D, MAPS3D are not applicable for this case.

            # Histograms look best from perspective when there is only one mapped spatial dimensions
            if self._plot_type == "HISTOGRAM":
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "perspective", "export")

            # For each of these cases, the following views are optimal and look better than "ortho"
            if self.x is not None:
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "top", "export")
            elif self.y is not None:
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "right", "export")
            else:
                return utils.case_insensitive_match(utils.EXPORT_VIEWS, "top", "export")

    # region PlotName
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if val is None:
            self._name = None
            return
        if isinstance(val, str):
            self._name = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "name",
                                                   "must be a 'str' specifying the desired name of the plot")
    
    @name.deleter
    def name(self):
        self.name = None
    # endregion PlotName

    # region LogLevel
    @property
    def log_level(self):
        """
        :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug

        :return: :class:`int`
        """
        return self._log_level

    @log_level.setter
    def log_level(self, val):
        """
        :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug

        :param val: :class:`int` from 0 to 2.
        :return: :class:`None`
        """
        if val in [0, 1, 2]:
            if val == 1:
                print("Setting log_level to 'help mode'")
            if val == 2:
                print("Setting log_level to 'debug mode'")
            self._log_level = val
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "log_level", "must be an 'int' from 0 to 2. "
                                                                                "0: quiet, 1: help, 2: debug")

    @log_level.deleter
    def log_level(self):
        """
        Sets the log_level to 0 ("quiet mode")

        :return: :class:`None`
        """
        print("Setting log_level to 'quiet mode'")
        self._log_level = 0

    # endregion LogLevel

    # region DataSetName
    @property
    def data_set_name(self):
        """
        :class:`str` Name of the dataset to use when creating the plot. default: :class:`None` implies use the
        currently loaded dataset.

        :return: :class:`str`
        """
        return self._data_set_name

    @data_set_name.setter
    def data_set_name(self, val):
        """
        :class:`str` Name of the dataset to use when creating the plot. default: :class:`None` implies use the
        currently loaded dataset.

        :param val: :class:`str`; must be the name of a dataset loaded in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._data_set_name = None
            return

        if isinstance(val, str):
            self._data_set_name = val
            if self.log_level >= api.LOG_DEBUG_LEVEL:
                print("'data_set_name' set to '{}'".format(val))
        else:
            utils.raise_invalid_argument_exception(str(type(val)), "data_set_name",
                                                   "must be a 'str' and correspond to the name of a dataset loaded "
                                                   "into VIP.")

    @data_set_name.deleter
    def data_set_name(self):
        """
        Sets the data_set_name to :class:`None` which implies that any requested plots should use the currently
        loaded dataset in VIP.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'data_set_name' has been set to 'None'; 'None' value implies the specified plot is "
                  "meant to be generated with whichever data set is currently loaded in VIP.")
        self._data_set_name = None

    # endregion DataSetName

    # region PlotType
    def plot_type(self, val):
        """
        Changes the plot type for the object. The passed value must be a :class:`str` and the valid values are
        {"scatter", "histogram", "line", "violin", "ellipsoid", "convex_hull", "surface", "maps2d", "maps3d"}. Default
        value of :class:`None` implies "scatter" plot, which is the default plot type in VIP. Changing the plot type
        may clear some plot settings based on the state of the plot object with the old plot type. This is to ensure
        that an illegal VipPlot object instance is not created.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            val = "SCATTER_PLOT"

        val = utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, val, "plot_type")

        if self._plot_type is not None and val == self._plot_type:
            return

        # First lets clear any plot settings from the previous plot type
        if val is not "HISTOGRAM":
            del self.x_bins, self.y_bins, self.z_bins, self.hist_volume_by
        if val is not "CONFIDENCE_ELLIPSOID":
            del self.confidence
        if val not in ["CONFIDENCE_ELLIPSOID", "SURFACE", "CONVEX_HULL"]:
            del self.show_points
        if val is not "MAPS2D":
            del self.map_provider, self.map_style
        if val is not "MAPS3D":
            del self.lat_long_lines, self.globe_style, self.country_lines, self.country_labels
        if val not in ["MAPS3D", "MAPS2D"]:
            del self.heatmap_enabled, self.heatmap_detail
        if val is not "LINE_PLOT":
            del self.viewby

        # Now lets clear any plot settings that are not applicable to the new plot type
        if val in ["MAPS2D", "MAPS3D"]:
            del self.x_scale, self.x_normalization, self.y_scale, self.y_normalization
        if val in ["HISTOGRAM", "LINE_PLOT", "CONFIDENCE_ELLIPSOID", "CONVEX_HULL"]:
            if self.color_type == "COLOR_GRADIENT":
                self.color_type = utils.case_insensitive_match(utils.COLOR_OPTIONS, "bins", "color_type")

        self._plot_type = val

        # Now lets set any default settings that are required by VIP
        if val == "CONFIDENCE_ELLIPSOID":
            self.confidence = 95.0
            self.show_points = True
        if val == "SURFACE":
            self.show_points = False
        if val == "CONVEX_HULL":
            self.show_points = True

    def get_plot_type(self):
        """
        Getter for the hidden attribute that is managed by the `plot_type(val)` method.

        :return: :class:`str`
        """
        return self._plot_type

    # endregion PlotType

    # region Dimensions

    @property
    def x(self):
        """
        X dimension (Spatial dimension). Should be set to :class:`str` of the feature name to be mapped to X
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that X dimension will
        not be mapped.

        :return: :class:`str` feature name to map to X dimension.
        """
        return self._x

    @x.setter
    def x(self, val):
        """
        X dimension (Spatial dimension). Should be set to :class:`str` of the feature name to be mapped to X
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that X dimension will
        not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to X
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._x = None
            del self.x_bins, self.x_scale, self.x_normalization
            return

        self._x = utils.get_name(val)
        if self.log_level > 1:
            print("'x' set to '{}'".format(self._x))

    @x.deleter
    def x(self):
        """
        Sets the X dimension to :class:`None` which implies that X dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'x' set to 'None'; 'None' value implies that nothing is to be mapped to the X "
                  "dimension. ")
        self.x = None

    @property
    def y(self):
        """
        Y dimension (Spatial dimension). Should be set to :class:`str` of the feature name to be mapped to Y
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that Y dimension will
        not be mapped.

        :return: :class:`str` feature name to map to Y dimension.
        """
        return self._y

    @y.setter
    def y(self, val):
        """
        Y dimension (Spatial dimension). Should be set to :class:`str` of the feature name to be mapped to Y
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that Y dimension will
        not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to Y
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._y = None
            del self.y_bins, self.y_scale, self.y_normalization
            return

        self._y = utils.get_name(val)
        if self.log_level > 1:
            print("'y' set to '{}'".format(self._y))

    @y.deleter
    def y(self):
        """
        Sets the Y dimension to :class:`None` which implies that Y dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'y' set to 'None'; 'None' value implies that nothing is to be mapped to the Y "
                  "dimension. ")
        self.y = None

    @property
    def z(self):
        """
        Z dimension (Spatial dimension). Should be set to :class:`str` of the feature name to be mapped to Z
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that Z dimension will
        not be mapped.

        :return: :class:`str` feature name to map to Z dimension.
        """
        return self._z

    @z.setter
    def z(self, val):
        """
        Z dimension (Spatial dimension). Should be set to :class:`str` of the feature name to be mapped to Z
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that Z dimension will
        not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to Z
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._z = None
            del self.z_bins, self.z_scale, self.z_normalization
            return

        self._z = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'z' set to '{}'".format(self._z))

    @z.deleter
    def z(self):
        """
        Sets the Z dimension to :class:`None` which implies that Z dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'z' set to 'None'; 'None' value implies that nothing is to be mapped to the Z "
                  "dimension. ")
        self.z = None

    @property
    def color(self):
        """
        Color dimension (appearance dimension). Should be set to :class:'str' of the feature name to be mapped to
        color dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that color
        dimension will not be mapped. Default color type depends on column type (continuous or categorical).

        :return: :class:`str` feature name to map to color dimension
        """
        return self._color

    @color.setter
    def color(self, val):
        """
        Color dimension (appearance dimension). Should be set to :class:'str' of the feature name to be mapped to
        color dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that color
        dimension will not be mapped. Default color type depends on column type (continuous or categorical).

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to color
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._color = None
            del self.color_bin_dist, self.color_type, self.color_normalization
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "color",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._color = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'color' set to '{}'".format(self._color))

    @color.deleter
    def color(self):
        """
        Sets the color dimension to :class:`None` which implies that color dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'color' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "color dimension. ")
        self.color = None

    @property
    def size(self):
        """
        Size dimension (appearance dimension). Should be set to :class:'str' of the feature name to be mapped to
        size dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that size dimension
        will not be mapped.

        :return: :class:`str`
        """
        return self._size

    @size.setter
    def size(self, val):
        """
        Size dimension (appearance dimension). Should be set to :class:'str' of the feature name to be mapped to
        size dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match
        a feature name in the specified dataset in VIP. Default is :class:`None` which implies that size dimension
        will not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to size
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._size = None
            del self.size_normalization, self.size_scale
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "size",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._size = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'size' set to '{}'".format(self._size))

    @size.deleter
    def size(self):
        """
        Sets the size dimension to :class:`None` which implies that size dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'size' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "size dimension.")
        self.size = None

    @property
    def shape(self):
        """
        Shape dimension (appearance dimension). Should be set to :class:`str` of the feature name to be mapped to
        shape dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that shape
        dimension will not be mapped.

        :return: :class:`str`
        """
        return self._shape

    @shape.setter
    def shape(self, val):
        """
        Shape dimension (appearance dimension). Should be set to :class:`str` of the feature name to be mapped to
        shape dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that shape
        dimension will not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to shape
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._shape = None
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "shape",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._shape = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'shape' set to '{}'".format(self._shape))

    @shape.deleter
    def shape(self):
        """
        Sets the shape dimension to :class:`None` which implies that shape dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'shape' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "shape dimension. ")
        self.shape = None

    @property
    def groupby(self):
        """
        Groupby dimension (refine dimension). Should be set to :class:`str` of the feature name to be mapped to
        groupby dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP.  Default is :class:`None` which implies that groupby
        dimension will not be mapped.

        :return: :class:`str`
        """
        return self._groupby

    @groupby.setter
    def groupby(self, val):
        """
        Groupby dimension (refine dimension). Should be set to :class:`str` of the feature name to be mapped to
        groupby dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP.  Default is :class:`None` which implies that groupby
        dimension will not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to groupby
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._groupby = None
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "groupby",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._groupby = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'groupby' set to '{}'".format(self._groupby))

    @groupby.deleter
    def groupby(self):
        """
        Sets groupby dimension to :class:`None` which implies that groupby dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'groupby' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "groupby dimension. ")
        self.groupby = None

    @property
    def playback(self):
        """
        Playback dimension (refine dimension). Should be set to :class:`str` of the feature name to be mapped to
        playback dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that playback
        dimension will not be mapped.

        :return: :class:`str`
        """
        return self._playback

    @playback.setter
    def playback(self, val):
        """
        Playback dimension (refine dimension). Should be set to :class:`str` of the feature name to be mapped to
        playback dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that playback
        dimension will not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to playback
        dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._playback = None
            del self.playback_highlight
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "playback",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._playback = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'playback' set to '{}'".format(self._playback))

    @playback.deleter
    def playback(self):
        """
        Sets playback dimension to :class:`None` which implies that playback dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'playback' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "playback dimension. ")
        self.playback = None

    @property
    def transparency(self):
        """
        Transparency dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to
        transparency dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and
        must match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that
        transparency dimension will not be mapped.

        :return: :class:`str`
        """
        return self._transparency

    @transparency.setter
    def transparency(self, val):
        """
        Transparency dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to
        transparency dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and
        must match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that
        transparency dimension will not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to
        transparency dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._transparency = None
            del self.transparency_normalization, self.transparency_scale
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "transparency",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._transparency = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'transparency' set to '{}'".format(self._transparency))

    @transparency.deleter
    def transparency(self):
        """
        Sets transparency dimension to :class:`None` which implies that the transparency dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'transparency' is set to 'None'; 'None' value implies that nothing is to be mapped to the"
                  "transparency dimension. ")
        self.transparency = None

    @property
    def halo(self):
        """
        Halo dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to halo
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match a
        feature name in the specified dataset in VIP. Default is :class:`None` which implies that halo dimension will
        not be mapped.

        :return: :class:`str`
        """
        return self._halo

    @halo.setter
    def halo(self, val):
        """
        Halo dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to halo
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match a
        feature name in the specified dataset in VIP. Default is :class:`None` which implies that halo dimension will
        not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to
        halo dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._halo = None
            del self.halo_scale, self.halo_highlight
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "halo",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._halo = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'halo' set to '{}'".format(self._halo))

    @halo.deleter
    def halo(self):
        """
        Sets halo dimension to :class:`None` which implies that the halo dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'halo' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "halo dimension. ")
        self.halo = None

    @property
    def pulsation(self):
        """
        Pulsation dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to
        pulsation dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that pulsation
        dimension will not be mapped.

        :return: :class:`str`
        """
        return self._pulsation

    @pulsation.setter
    def pulsation(self, val):
        """
        Pulsation dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to
        pulsation dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must
        match a feature name in the specified dataset in VIP. Default is :class:`None` which implies that pulsation
        dimension will not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to
        pulsation dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._pulsation = None
            del self.pulsation_highlight
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "pulsation",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._pulsation = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'pulsation' set to '{}'".format(self._pulsation))

    @pulsation.deleter
    def pulsation(self):
        """
        Sets pulsation dimension to :class:`None` which implies that the pulsation dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'pulsation' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "pulsation dimension. ")
        self.pulsation = None

    @property
    def arrow(self):
        """
        Arrow dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to arrow
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match a
        feature name in the specified dataset in VIP. Default is :class:`None` which implies that arrow dimension will
        not be mapped.

        :return: :class:`str`
        """
        return self._arrow

    @arrow.setter
    def arrow(self, val):
        """
        Arrow dimension (Extra dimension). Should be set to :class:`str` of the feature name to be mapped to arrow
        dimension in VIP. If a :class:`pandas.Series` is passed, the `name` attribute will be used and must match a
        feature name in the specified dataset in VIP. Default is :class:`None` which implies that arrow dimension will
        not be mapped.

        :param val: :class:`str` or :class:`pandas.Series` containing the name of the feature to be mapped to
        arrow dimension in VIP.
        :return: :class:`None`
        """
        if val is None:
            self._arrow = None
            del self.arrow_normalization, self.arrow_scale
            return

        if not self.is_spatial_dimension_used():
            utils.raise_invalid_argument_exception(str(type(val)), "arrow",
                                                   "One of the spatial dimensions (X, Y, or Z) must be mapped "
                                                   "before the other dimensions can be used.")
        self._arrow = utils.get_name(val)
        if self.log_level >= api.LOG_DEBUG_LEVEL:
            print("'arrow' set to '{}'".format(self._arrow))

    @arrow.deleter
    def arrow(self):
        """
        Sets arrow dimension to :class:`None` which implies that the arrow dimension will not be mapped.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'arrow' is set to 'None'; 'None' value implies that nothing is to be mapped to the "
                  "arrow dimension. ")
        self.arrow = None

    # endregion

    # region PlotSettings

    # region Scaling
    @property
    def x_scale(self):
        """
        X scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP to
        default scaling value. X scale is only applicable when the X dimension is being used. X scale is not
        applicable for Geospatial plot types ('maps2d', 'maps3d').

        :return: :class:`float`
        """
        return self._x_scale

    @x_scale.setter
    def x_scale(self, val):
        """
        X scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP to
        default scaling value. X scale is only applicable when the X dimension is being used. X scale is not
        applicable for Geospatial plot types ('maps2d', 'maps3d').

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._x_scale = None
            return

        if self.x is None:
            utils.raise_invalid_argument_exception(str(type(val)), "x_scale",
                                                   "'x_scale' is only applicable if 'x' has been mapped.")
        if self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "x_scale",
                                                   "'x_scale' is not applicable for geospatial plots. ")

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "x_scale", "must be a 'float' between .5 and 5")

        self._x_scale = val

    @x_scale.deleter
    def x_scale(self):
        """
        Sets the X scale setting to 'None'; VIP will proceed to use the default X scaling as a result.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'x_scale' is set to 'None': 'None' value implies the default scale value will be used.")
        self.x_scale = None

    @property
    def y_scale(self):
        """
        Y scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP to
        default scaling value. Y scale is only applicable when the Y dimension is being used. Y scale is not
        applicable for Geospatial plot types ('maps2d', 'maps3d').

        :return: :class:`float`
        """
        return self._y_scale

    @y_scale.setter
    def y_scale(self, val):
        """
        Y scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP to
        default scaling value. Y scale is only applicable when the Y dimension is being used. Y scale is not
        applicable for Geospatial plot types ('maps2d', 'maps3d').

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._y_scale = None
            return

        if self.y is None:
            utils.raise_invalid_argument_exception(str(type(val)), "y_scale",
                                                   "'y_scale' is only applicable if 'y' has been mapped.")
        if self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "y_scale",
                                                   "'y_scale' is not applicable for geospatial plots. ")

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "y_scale", "must be a 'float' between .5 and 5")

        self._y_scale = val

    @y_scale.deleter
    def y_scale(self):
        """
        Sets the Y scale setting to 'None'; VIP will proceed to use the default Y scaling as a result.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'y_scale' is set to 'None': 'None' value implies the default scale value will be used.")
        self.y_scale = None

    @property
    def z_scale(self):
        """
        Z scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP to
        default scaling value. Z scale is only applicable when the Z dimension is being used.

        :return: :class:`float`
        """
        return self._z_scale

    @z_scale.setter
    def z_scale(self, val):
        """
        Z scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP to
        default scaling value. Z scale is only applicable when the Z dimension is being used.

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._z_scale = None
            return

        if self.z is None:
            utils.raise_invalid_argument_exception(str(type(val)), "z_scale",
                                                   "'z_scale' is only applicable if 'z' has been mapped.")

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "z_scale", "must be a 'float' between .5 and 5")

        self._z_scale = val

    @z_scale.deleter
    def z_scale(self):
        """
        Sets the Z scale setting to 'None'; VIP will proceed to use the default Z scaling as a result.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'z_scale' is set to 'None': 'None' value implies the default scale value will be used.")
        self.z_scale = None

    @property
    def size_scale(self):
        """
        Size scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP
        to default scaling value.

        :return: :class:`float`
        """
        return self._size_scale

    @size_scale.setter
    def size_scale(self, val):
        """
        Size scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None' leaves VIP
        to default scaling value.

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._size_scale = None
            return

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "size_scale", "must be a 'float' between .5 and 5")

        self._size_scale = val

    @size_scale.deleter
    def size_scale(self):
        """
        Sets size scale to 'None'; VIP will proceed to use the default size setting

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'size_scale' is set to 'None': 'None' value implies the default scale value will be "
                  "used. ")
        self.size_scale = None

    @property
    def transparency_scale(self):
        """
        Transparency scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None'
        leaves VIP to default scaling value.

        :return: :class:`float`
        """
        return self._transparency_scale

    @transparency_scale.setter
    def transparency_scale(self, val):
        """
        Transparency scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None'
        leaves VIP to default scaling value.

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._transparency_scale = None
            return

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "transparency_scale", "must be a 'float' between .5 and 5")

        self._transparency_scale = val

    @transparency_scale.deleter
    def transparency_scale(self):
        """
        Sets transparency scale to 'None'; VIP will proceed to use the default size setting

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'transparency_scale' is set to 'None': 'None' value implies the default scale value will "
                  "be used. ")
        self.transparency_scale = None

    @property
    def halo_scale(self):
        """
        Halo scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None'
        leaves VIP to default scaling value.

        :return: :class:`float`
        """
        return self._halo_scale

    @halo_scale.setter
    def halo_scale(self, val):
        """
        Halo scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None'
        leaves VIP to default scaling value.

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._halo_scale = None
            return

        if self.halo is None:
            utils.raise_invalid_argument_exception(str(type(val)), "halo",
                                                   "'halo_scale' is only appliable when 'halo' dimension has been "
                                                   "mapped. ")

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "halo_scale", "must be a 'float' between .5 and 5")

        self._halo_scale = val

    @halo_scale.deleter
    def halo_scale(self):
        """
        Sets halo scale to 'None'; VIP will proceed to use the default size setting

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'halo_scale' is set to 'None': 'None' value implies the default scale value will "
                  "be used. ")
        self.halo_scale = None

    @property
    def arrow_scale(self):
        """
        Arrow scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None'
        leaves VIP to default scaling value.

        :return: :class:`float`
        """
        return self._arrow_scale

    @arrow_scale.setter
    def arrow_scale(self, val):
        """
        Arrow scale setting. Must be set to :class:`float` with value between .5 and 5. Default value 'None'
        leaves VIP to default scaling value.

        :param val: :class:`float` between .5 and 5
        :return: :class:`None`
        """
        if (val is None) or (val == 1):
            self._arrow_scale = None
            return

        if self.arrow is None:
            utils.raise_invalid_argument_exception(str(type(val)), "arrow",
                                                   "'arrow_scale' is only applicable when 'arrow' dimension has been "
                                                   "mapped. ")

        if not isinstance(val, float) or not .5 <= val <= 5:
            utils.raise_invalid_argument_exception(
                str(type(val)), "arrow_scale", "must be a 'float' between .5 and 5")

        self._arrow_scale = val

    @arrow_scale.deleter
    def arrow_scale(self):
        """
        Sets arrow scale to 'None'; VIP will proceed to use the default size setting

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'arrow_scale' is set to 'None': 'None' value implies the default scale value will "
                  "be used. ")
        self.arrow_scale = None

    # endregion Scaling

    # region Color Settings
    @property
    def color_type(self):
        """
        Color type setting. Must be set to :class:`str` and match one of the following {"gradient", "bin", "palette",
        None}. Default value 'None' leaves VIP to default color type based, which is dependent on the feature mapped
        to color. Color type setting is only applicable when the 'color' dimension has been mapped.

        :return: :class:`str`
        """
        return self._color_type

    @color_type.setter
    def color_type(self, val):
        """
        Color type setting. Must be set to :class:`str` and match one of the following {"gradient", "bin", "palette",
        None}. Default value 'None' leaves VIP to default color type based, which is dependent on the feature mapped
        to color. Color type setting is only applicable when the 'color' dimension has been mapped.

        :param val: :class:`str` that matches one of the following {"gradient", "bin", "palette", None}
        :return: :class:`None`
        """
        if val is None:
            self._color_type = None
            del self.color_bin_dist, self.color_bins
            return

        if self.color is None:
            utils.raise_invalid_argument_exception(
                str(type(val)), 'color_type', "'color_type' is only applicable when the 'color' dimension is mapped. ")

        val = utils.case_insensitive_match(utils.COLOR_OPTIONS, val, "color_type")

        if hasattr(self, '_color_type') and val == self._color_type:
            return

        if self._plot_type == "CONFIDENCE_ELLIPSOID" and val not in ["COLOR_BIN", "COLOR_PALETTE"]:
            utils.raise_invalid_argument_exception(str(type(val)), "color_type",
                                                   "when 'plot_type' is 'CONFIDENCE_ELLIPSOID', 'color_type' must "
                                                   "be set to 'COLOR_BIN' or 'COLOR_PALETTE'")

        if self._plot_type == "CONVEX_HULL" and val not in ["COLOR_BIN", "COLOR_PALETTE"]:
            utils.raise_invalid_argument_exception(str(type(val)), "color_type",
                                                   "when 'plot_type' is 'CONVEX_HULL', 'color_type' must "
                                                   "be set to 'COLOR_BIN' or 'COLOR_PALETTE'")

        if self._plot_type == "LINE_PLOT" and val not in ["COLOR_BIN", "COLOR_PALETTE"] and self.viewby == "ByColor":
            utils.raise_invalid_argument_exception(str(type(val)), "color_type",
                                                   "when 'plot_type' is 'LINE_PLOT' and `viewby` is `Color`, "
                                                   "'color_type' must be set to 'COLOR_BIN' or 'COLOR_PALETTE'")

        if self._plot_type == "HISTOGRAM" and val not in ["COLOR_BIN", "COLOR_PALETTE"]:
            utils.raise_invalid_argument_exception(str(type(val)), "color_type",
                                                   "when 'plot_type' is 'HISTOGRAM', 'color_type' must "
                                                   "be set to 'COLOR_BIN' or 'COLOR_PALETTE'")

        if val != "COLOR_BIN":
            del self.color_bin_dist, self.color_bins
        if val != "COLOR_GRADIENT":
            del self.color_normalization

        self._color_type = val

    @color_type.deleter
    def color_type(self):
        """
        Sets color_type to 'None' which means VIP will be set to default color type, which is dependent on the
        feature mapped to color dimension.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'color_type' set to 'None'; 'None' value implies that VIP will use the default color"
                  " type for the feature mapped to 'color' dimension. ")
        self.color_type = None

    @property
    def color_bins(self):
        """
        Color bin setting. Must be set to :class:`int` between 1 and 16. The color bin setting is only applicable
        when 'color' dimension has been mapped. Default value of 'None' will set color bins to the min(unique values
        of the feature mapped to color, 4).

        :return: :class:`int`
        """
        return self._color_bins

    @color_bins.setter
    def color_bins(self, val):
        """
        Color bin setting. Must be set to :class:`int` between 1 and 16. The color bin setting is only applicable
        when 'color' dimension has been mapped. Default value of 'None' will set color bins to the min(unique values
        of the feature mapped to color, 4).

        :param val: :class:`int` between 1 and 16
        :return: :class:`None`
        """
        if val is None:
            self._color_bins = None
            return

        if self.color is None:
            utils.raise_invalid_argument_exception(str(type(val)), 'color_bins',
                                                   "'color_bins' is only applicable if the 'color' dimension has been"
                                                   " mapped. ")

        if self.color_type not in ["COLOR_BIN"]:
            utils.raise_invalid_argument_exception(str(type(val)), 'color_bins',
                                                   "'color_bins' is only applicable when 'color_type' is *explicitly* "
                                                   "set to 'COLOR_BIN' or an appropriate alias.")
        
        if (not isinstance(val, int)) or (not 1 <= val <= 16):
            utils.raise_invalid_argument_exception(str(type(val)), 'color_bins',
                                                   "'color_bins' must be be set to an 'int' between 1 and 16. ")

        self._color_bins = val

    @color_bins.deleter
    def color_bins(self):
        """
        Sets color bin to 'None'; VIP will leave the number of color bins to the default, which is dependent on the
        number of unique values in the feature mapped to 'color' dimension

        :return: :class:`None`
        """
        self.color_bins = None

    @property
    def color_bin_dist(self):
        """
        Color bin distribution setting. Must be a :class:`str` that matches one of {"equal", "range}. Default of
        'None' leaves the color bin distribution in VIP as default ('equal'). Color bin distribution is only
        applicable when a feature has been mapped 'color'

        :return: :class:`str`
        """
        return self._color_bin_dist

    @color_bin_dist.setter
    def color_bin_dist(self, val):
        """
        Color bin distribution setting. Must be a :class:`str` that matches one of {"equal", "range}. Default of
        'None' leaves the color bin distribution in VIP as default ('equal'). Color bin distribution is only
        applicable when a feature has been mapped 'color'

        :param val: :class:`str` that matches one of {"equal", "range}
        :return: :class:`None`
        """
        if val is None:
            self._color_bin_dist = None
            return

        if self.color is None:
            utils.raise_invalid_argument_exception(str(type(val)), 'color_bin_dist',
                                                   "'color_bin_dist' is only applicable if the 'color' dimension has "
                                                   "been mapped. ")

        if self.color_type not in ["COLOR_BIN"]:
            utils.raise_invalid_argument_exception(str(type(val)), 'color_bin_dist',
                                                   "'color_bin_dist' is only applicable when 'color_type' is "
                                                   "*explicitly* set to 'COLOR_BIN' or an appropriate alias.")

        self._color_bin_dist = utils.case_insensitive_match(utils.COLOR_BIN_MODES, val, "color_bin_dist")

    @color_bin_dist.deleter
    def color_bin_dist(self):
        """
        Sets color bin distribution to 'None'; VIP will leave the bin distribution to the default ('equal').

        :return: :class:`None`
        """
        self._color_bin_dist = None

    @property
    def color_inverted(self):
        """
        Color Inversion state. Must be a :class:`bool`. Default of `False` leaves the color bins, palette, or gradient
        as is. Value of `True` inverts the color order regardless of color type. Color inversion is only applicable
        when a feature has been mapped to 'color'

        :return: :class:`None`
        """
        return self._color_inverted

    @color_inverted.setter
    def color_inverted(self, val):
        """
        Color Inversion state. Must be a :class:`bool`. Default of `False` leaves the color bins, palette, or gradient
        as is. Value of `True` inverts the color order regardless of color type. Color inversion is only applicable
        when a feature has been mapped to 'color'

        :return: :class:`None`
        """
        if val is None:
            self._color_inverted = None
            return

        if type(val) is not bool:
            utils.raise_invalid_argument_exception(str(type(val)), "color_inverted",
                                                   "'color_inverted' must be a boolean value: True or False")

        if self.color is None:
            if self._plot_type is not "HISTOGRAM":
                utils.raise_invalid_argument_exception(str(type(val)), "color_inverted",
                                                   "'color_inverted' is only applicable when 'color' dimension has "
                                                   "been mapped or when plotting a histogram. ")

        self._color_inverted = val

    @color_inverted.deleter
    def color_inverted(self):
        """
        Sets color inversion state to False. VipPlots will use the default color ordering.

        :return: :class:`None`
        """
        self._color_inverted = False

    # endregion Color Settings

    # region Normalization
    @property
    def x_normalization(self):
        """
        X normalization setting. Must be set to :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. X normalization is only applicable when 'x' dimension is mapped.
        X normalization is not applicable for Geospatial plots.

        :return: :class:`str`
        """
        return self._x_normalization

    @x_normalization.setter
    def x_normalization(self, val):
        """
        X normalization setting. Must be set to :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. X normalization is only applicable when 'x' dimension is mapped.
        X normalization is not applicable for Geospatial plots.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._x_normalization = None
            return

        if self.x is None:
            utils.raise_invalid_argument_exception(str(type(val)), "x_normalization",
                                                   "'x_normalization' is only applicable when the 'x' dimension is "
                                                   "mapped. ")

        if self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "x_normalization",
                                                   "'x_normalization' is not applicable for Geospatial plots. ")

        self._x_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val, "x_normalization")

    @x_normalization.deleter
    def x_normalization(self):
        """
        Sets X normalization setting to 'None': normalization will not be applied to 'x' dimension`

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'x_normalization' is set to 'None': normalization will not be applied to the x"
                  " dimension.")
        self.x_normalization = None

    @property
    def y_normalization(self):
        """
        Y normalization setting. Must be set to :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. Y normalization is only applicable when 'y' dimension is mapped.
        Y normalization is not applicable for Geospatial plots.

        :return: :class:`str`
        """
        return self._y_normalization

    @y_normalization.setter
    def y_normalization(self, val):
        """
        Y normalization setting. Must be set to :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. Y normalization is only applicable when 'y' dimension is mapped.
        Y normalization is not applicable for Geospatial plots.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._y_normalization = None
            return

        if self.y is None:
            utils.raise_invalid_argument_exception(str(type(val)), "y_normalization",
                                                   "'y_normalization' is only applicable when the 'y' dimension is "
                                                   "mapped. ")

        if self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "y_normalization",
                                                   "'y_normalization' is not applicable for Geospatial plots. ")

        self._y_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val, "y_normalization")

    @y_normalization.deleter
    def y_normalization(self):
        """
        Sets Y normalization setting to 'None': normalization will not be applied to 'y' dimension`

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'y_normalization' is set to 'None': normalization will not be applied to the 'y'"
                  " dimension.")
        self.y_normalization = None

    @property
    def z_normalization(self):
        """
        Z normalization setting. Must be set to :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. Z normalization is only applicable when 'z' dimension is mapped.
        Z normalization is not applicable for Geospatial plots.

        :return: :class:`str`
        """
        return self._z_normalization

    @z_normalization.setter
    def z_normalization(self, val):
        """
        Z normalization setting. Must be set to :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. Z normalization is only applicable when 'z' dimension is mapped.
        Z normalization is not applicable for Geospatial plots.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._z_normalization = None
            return

        if self.z is None:
            utils.raise_invalid_argument_exception(str(type(val)), "z_normalization",
                                                   "'z_normalization' is only applicable when the 'z' dimension is "
                                                   "mapped. ")

        self._z_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val, "z_normalization")

    @z_normalization.deleter
    def z_normalization(self):
        """
        Sets Y normalization setting to 'None': normalization will not be applied to 'y' dimension`

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'z_normalization' is set to 'None': normalization will not be applied to the 'z'"
                  " dimension.")
        self.z_normalization = None

    @property
    def color_normalization(self):
        """
        Color normalization setting. Must be set :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. Color normalization is only applicable when 'color' dimension is
        mapped and color type has been set to 'gradient.' Default is 'None' which implies that normalization will
        not be applied to 'color' dimension.

        :return: :class:`str`
        """
        return self._color_normalization

    @color_normalization.setter
    def color_normalization(self, val):
        """
        Color normalization setting. Must be set :class:`str` and match with one of the Normalization options listed
        here: {"Softmax", "Log10", "IHST", None}. Color normalization is only applicable when 'color' dimension is
        mapped and color type has been set to 'gradient.' Default is 'None' which implies that normalization will
        not be applied to 'color' dimension.

        :param val: :class:`str`
        :return: :class:`str`
        """
        if val is None:
            self._color_normalization = None
            return

        if self.color is None:
            utils.raise_invalid_argument_exception(str(type(val)), "color_normalization",
                                                   "'color_normalization' is only applicable when a feature has been "
                                                   "mapped to the 'color' dimension.")

        if self.color_type is not "COLOR_GRADIENT":
            utils.raise_invalid_argument_exception(str(type(val)), "color_normalization",
                                                   "'color_normalization' is only applicable when 'color_type' has "
                                                   "been set to 'gradient'")

        self._color_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val,
                                                                 "color_normalization")

    @color_normalization.deleter
    def color_normalization(self):
        """
        Sets color normalization to 'None'; VIP will not apply normalization to 'color' dimension.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'color_normalization' is set to 'None': normalization will not be applied to the 'color'"
                  " dimension. ")
        self.color_normalization = None

    @property
    def size_normalization(self):
        """
        Size normalization setting. Must be set :class:`str` and match with one of the normalization options listed
        here: {"softmax", "Log10", "IHST", None}. Size normalization is only applicable when 'size' dimension has
        been mapped. Default is 'None' which implies that normalization will not be applied to the 'size' dimension.

        :return: :class:`str`
        """
        return self._size_normalization

    @size_normalization.setter
    def size_normalization(self, val):
        """
        Size normalization setting. Must be set :class:`str` and match with one of the normalization options listed
        here: {"softmax", "Log10", "IHST", None}. Size normalization is only applicable when 'size' dimension has
        been mapped. Default is 'None' which implies that normalization will not be applied to the 'size' dimension.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._size_normalization = None
            return

        if self.size is None:
            utils.raise_invalid_argument_exception(str(type(val)), "size_normalization",
                                                   "'size_normalization' is only applicable when a feature has been "
                                                   "mapped to the 'size' dimension.")

        self._size_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val, "size_normalization")

    @size_normalization.deleter
    def size_normalization(self):
        """
        Sets size normalization to 'None'; VIP will not apply normalization to the 'size' dimension.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'size_normalization' is set to 'None': normalization will not be applied to the 'size'"
                  " dimension")
        self.size_normalization = None

    @property
    def transparency_normalization(self):
        """
        Transparency normalization setting. Must be set :class:`str` and match with one of the normalization options
        listed here: {"softmax", "Log10", "IHST", None}. Transparency normalization is only applicable when
        'transparency' dimension has been mapped. Default is 'None' which implies that normalization will not be
        applied to the 'transparency' dimension.

        :return: :class:`str`
        """
        return self._transparency_normalization

    @transparency_normalization.setter
    def transparency_normalization(self, val):
        """
        Transparency normalization setting. Must be set :class:`str` and match with one of the normalization options
        listed here: {"softmax", "Log10", "IHST", None}. Transparency normalization is only applicable when
        'transparency' dimension has been mapped. Default is 'None' which implies that normalization will not be
        applied to the 'transparency' dimension.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._transparency_normalization = None
            return

        if self.transparency is None:
            utils.raise_invalid_argument_exception(str(type(val)), "transparency_normalization",
                                                   "'transparency_normalization' is only applicable when a feature has "
                                                   "been mapped to the 'transparency' dimension.")

        self._transparency_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val,
                                                                        "transparency_normalization")

    @transparency_normalization.deleter
    def transparency_normalization(self):
        """
        Sets transparency normalization to 'None'; VIP will not apply normalization to the 'transparency' dimension.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'transparency_normalization' is set to 'None': normalization will not be applied to the "
                  "'transparency' dimension. ")
        self.transparency_normalization = None

    @property
    def arrow_normalization(self):
        """
        Arrow normalization setting. Must be set :class:`str` and match with one of the normalization options
        listed here: {"softmax", "Log10", "IHST", None}. Arrow normalization is only applicable when
        'arrow' dimension has been mapped. Default is 'None' which implies that normalization will not be
        applied to the 'arrow' dimension.

        :return: :class:`str`
        """
        return self._arrow_normalization

    @arrow_normalization.setter
    def arrow_normalization(self, val):
        """
        Arrow normalization setting. Must be set :class:`str` and match with one of the normalization options
        listed here: {"softmax", "Log10", "IHST", None}. Arrow normalization is only applicable when
        'arrow' dimension has been mapped. Default is 'None' which implies that normalization will not be
        applied to the 'arrow' dimension.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._arrow_normalization = None
            return

        if self.arrow is None:
            utils.raise_invalid_argument_exception(str(type(val)), "arrow_normalization",
                                                   "'arrow_normalization' is only applicable when a feature has "
                                                   "been mapped to the 'arrow' dimension.")

        self._arrow_normalization = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, val,
                                                                 "arrow_normalization")

    @arrow_normalization.deleter
    def arrow_normalization(self):
        """
        Sets arrow normalization to 'None'; VIP will not apply normalization to the 'transparency' dimension.

        :return:
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'arrow_normalization' is set to 'None': normalization will not be applied to the "
                  "'arrow' dimension. ")
        self.arrow_normalization = None

    # endregion Normalization

    # region GeospatialSettings

    # region 3DPlotSettings

    @property
    def globe_style(self):
        """
        Globe style setting. Must be set to :class:`str` that matches one of {"natural", "dark", "black ocean",
        "blue ocean", "gray ocean", "water color", "topographic", "moon", "night"}. Globe style setting
        is only applicable when 'plot_type' is set to "MAPS3D". Default is 'None' which implies VIP will use the
        default globe style.

        :return: :class:`str`
        """
        return self._globe_style

    @globe_style.setter
    def globe_style(self, val):
        """
        Globe style setting. Must be set to :class:`str` that matches one of {"natural", "dark", "black ocean",
        "blue ocean", "gray ocean", "water color", "topographic", "moon", "night"}. Globe style setting
        is only applicable when 'plot_type' is set to "MAPS3D". Default is 'None' which implies VIP will use the
        default globe style.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._globe_style = None
            return

        if self._plot_type is not "MAPS3D":
            utils.raise_invalid_argument_exception(str(type(val)), 'globe_style',
                                                   "'globe_style' is only applicable when 'plot_type' is 'MAPS3d'")

        val = utils.case_insensitive_match(utils.GLOBE_STYLE_OPTIONS, val, "globe_style")
        self._globe_style = val

    @globe_style.deleter
    def globe_style(self):
        """
        Sets globe style setting to 'None' which implies VIP will use the default globe style.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'globe_style' has been set to 'None'; VIP will use the default globe style. ")
        self.globe_style = None

    @property
    def lat_long_lines(self):
        """
        Latitude/Longitude Lines setting. Must be set to :class:`bool` or :class:`str` and match on of {"show", True,
        "hide", False}. 'lat_long_lines' is only applicable when the plot type is set to 'MAPS3D'. Default is 'None'
        which implies VIP will use the default for latitude/longitude lines.

        :return: :class:`bool`
        """
        return self._lat_long_lines

    @lat_long_lines.setter
    def lat_long_lines(self, val):
        """
        Latitude/Longitude Lines setting. Must be set to :class:`bool` or :class:`str` and match on of {"show", True,
        "hide", False}. 'lat_long_lines' is only applicable when the plot type is set to 'MAPS3D'. Default is 'None'
        which implies VIP will use the default for latitude/longitude lines.

        :param val: :class:`bool`
        :return: :class:`None`
        """
        if val is None:
            self._lat_long_lines = None
            return

        if self._plot_type is not "MAPS3D":
            utils.raise_invalid_argument_exception(str(type(val)), "lat_long_lines",
                                                   "'lat_long_lines' is only applicable when 'plot_type' is 'MAPS3D'")

        self._lat_long_lines = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, val, "lat_long_lines")

    @lat_long_lines.deleter
    def lat_long_lines(self):
        """
        Sets latitude/longitude lines to 'None'; VIP will use the default value for latitude/longitude line visibility.

        :return: :class:`bool`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'lat_long_lines' has been set to 'None'; VIP will use the default visibility for "
                  "latitude/longitude lines. ")
        self.lat_long_lines = None

    @property
    def country_lines(self):
        """
        Country Lines setting. Must be set to :class:`bool` or :class:`str` and match on of {"show", True,
        "hide", False}. 'country_lines' is only applicable when the plot type is set to 'MAPS3D'. Default is 'None'
        which implies VIP will use the default for country lines.

        :return: :class:`bool`
        """
        return self._country_lines

    @country_lines.setter
    def country_lines(self, val):
        """
        Country Lines setting. Must be set to :class:`bool` or :class:`str` and match on of {"show", True,
        "hide", False}. 'country_lines' is only applicable when the plot type is set to 'MAPS3D'. Default is 'None'
        which implies VIP will use the default for country lines.

        :param val: :class:`bool`
        :return: :class:`None`
        """
        if val is None:
            self._country_lines = None
            return

        if self._plot_type is not "MAPS3D":
            utils.raise_invalid_argument_exception(str(type(val)), "country_lines",
                                                   "'country_lines' is only applicable when 'plot_type' is 'MAPS3D'")

        self._country_lines = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, val, "country_lines")

    @country_lines.deleter
    def country_lines(self):
        """
        Sets country lines to 'None'; VIP will use the default value for the country lines.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'country_lines' has been set to 'None'; VIP will use the default visibility for "
                  "country lines. ")
        self.country_lines = None

    @property
    def country_labels(self):
        """
        Country labels setting. Must be set to :class:`bool` or :class:`str` and match on of {"show", True,
        "hide", False}. 'country_labels' is only applicable when the plot type is set to 'MAPS3D'. Default is 'None'
        which implies VIP will use the default for country labels.

        :return: :class:`bool`
        """
        return self._country_labels

    @country_labels.setter
    def country_labels(self, val):
        """
        Country labels setting. Must be set to :class:`bool` or :class:`str` and match one of {"show", True,
        "hide", False}. 'country_labels' is only applicable when the plot type is set to 'MAPS3D'. Default is 'None'
        which implies VIP will use the default for country labels.

        :param val: :class:`bool`
        :return: :class:`None`
        """
        if val is None:
            self._country_labels = None
            return

        if self._plot_type is not "MAPS3D":
            utils.raise_invalid_argument_exception(str(type(val)), "country_labels",
                                                   "'country_labels' is only applicable when 'plot_type' is 'MAPS3D'")

        val = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, val, "country_labels")
        self._country_labels = val

    @country_labels.deleter
    def country_labels(self):
        """
        Set country labels to 'None': VIP will use the default value for the country lines.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'country_labels' has been set to 'None'; VIP will use the default visibility for "
                  "country labels. ")
        self.country_labels = None

    # endregion 3DPlotSettings
    
    # region 2DPlotSettings
    
    @property
    def map_provider(self):
        """
        Map provider setting. Must be set to :class:`str` and match with one of {"ArcGIS", "Stamen", "OpenStreetMap"}
        or `None`, which is the default and sets VIP to use the default map provider for relevant plots. Map provider
        is only applicable when plot type is set to 'MAPS2D'.

        :return: :class`str`
        """
        return self._map_provider
    
    @map_provider.setter
    def map_provider(self, val):
        """
        Map provider setting. Must be set to :class:`str` and match with one of {"ArcGIS", "Stamen", "OpenStreetMap"}
        or `None`, which is the default and sets VIP to use the default map provider for relevant plots. Map provider
        is only applicable when plot type is set to 'MAPS2D'.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            self._map_provider = None
            del self.map_style
            return

        if self._plot_type is not "MAPS2D":
            utils.raise_invalid_argument_exception(str(type(val)), 'map_provider',
                                                   "'map_provider' is only applicable when 'plot_type' is 'MAPS2D'")

        self._map_provider = utils.case_insensitive_match(utils.MAP_PROVIDERS, val, "map_provider")
        self.map_style = None
    
    @map_provider.deleter
    def map_provider(self):
        """
        Sets map provider setting to `None`, which implies VIP will use the default map provider if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'map_provider' is set to 'None'; VIP will use the default map provider and map style")
        self.map_provider = None
    
    @property
    def map_style(self):
        """
        Map style settings. Must be set to :class:`str` and match one of the following depending on the map provider:
        ArcGIS: {"Topographic", "Ocean", "Imagery", "Gray"}, OpenStreetMap: {"Mapnik"},
        Stamen: {"Dark", "Light", "Watercolor", "Terrain"}
        Map style is only applicable when plot_type is set to 'MAPS2D'. The default is `None` which implies VIP will
        use the default map style for the currently set map provider.

        :return: :class:`str`
        """
        return self._map_style
    
    @map_style.setter
    def map_style(self, val):
        """
        Map style settings. Must be set to :class:`str` and match one of the following depending on the map provider:
        ArcGIS: {"Topographic", "Ocean", "Imagery", "Gray"}, OpenStreetMap: {"Mapnik"},
        Stamen: {"Dark", "Light", "Watercolor", "Terrain"}
        Map style is only applicable when plot_type is set to 'MAPS2D'. The default is `None` which implies VIP will
        use the default map style for the currently set map provider.

        :param val: :class:`str`
        :return: :class:`None`
        """
        if val is None:
            if self.map_provider is None:
                self._map_style = None
            else:
                style = utils.case_insensitive_match(utils.MAP_STYLES[self.map_provider], "default", "map_style")
                self._map_style = style
            return

        if self._plot_type is not "MAPS2D":
            utils.raise_invalid_argument_exception(str(type(val)), 'map_style',
                                                   "'map_style' is only applicable when 'plot_type' is 'MAPS2D'")

        # val = utils.case_insensitive_match()
        if self.map_provider is None:
            utils.raise_invalid_argument_exception(str(type(val)), "map_style",
                                                   "'map_style' is only applicable if 'map_provider' has already been"
                                                   " set. ")
        self._map_style = utils.case_insensitive_match(utils.MAP_STYLES[self.map_provider], val, "map_style")

    @map_style.deleter
    def map_style(self):
        """
        Sets map style to `None`; VIP will use the default map style for the currently set map provider, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'map_style' is set to 'None'; VIP will use the default map style for the specified "
                  "map provider. ")
        self.map_style = None
    
    # endregion 2DPlotSettings

    # region HeatmapSettings

    @property
    def heatmap_enabled(self):
        """
        Heatmap enabled setting. Must be set to :class:`bool`. Heatmaps are only applicable for geospatial plots.
        Default value is `None` which implies that VIP will not generate heatmap visualizations.

        :return: :class:`bool`
        """
        return self._heatmap_enabled

    @heatmap_enabled.setter
    def heatmap_enabled(self, val):
        """
        Heatmap enabled setting. Must be set to :class:`bool`. Heatmaps are only applicable for geospatial plots.
        Default value is `None` which implies that VIP will not generate heatmap visualizations.

        :param val: :class:`bool`
        :return: :class:`None`
        """
        if val is None:
            self._heatmap_enabled = None
            self.heatmap_detail = None
            return

        if not self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_enabled",
                                                   "'heatmap_enabled' is only applicable for Geospatial plot types. ")

        self._heatmap_enabled = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, val, "heatmap_enabled")

    @heatmap_enabled.deleter
    def heatmap_enabled(self):
        """
        Sets heatmap enabled to `None`; VIP will not generate a heatmap visualization

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'heatmap_enabled' is set to `None`; VIP will not generate heatmap visualization. ")
        self.heatmap_enabled = None

    @property
    def heatmap_intensity(self):
        """
        Heatmap intensity setting. Must be set to a :class:`float` between 0 and 1. Heatmaps are only applicable for
        geospatial plots. Heatmap intensity setting is only applicable if the heatmap_enabled is set to `True`.

        :return: :class:`float`
        """
        return self._heatmap_intensity

    @heatmap_intensity.setter
    def heatmap_intensity(self, val):
        """
        Heatmap intensity setting. Must be set to a :class:`float` between 0 and 1. Heatmaps are only applicable for
        geospatial plots. Heatmap intensity setting is only applicable if the heatmap_enabled is set to `True`.

        :param val: :class:`float`
        :return: :class:`None`
        """
        if (val is None) or (val == .5):
            self._heatmap_intensity = None
            return

        if not self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_intesity",
                                                   "'heatmap_intensity' is only applicable for Geospatial plot types. ")

        if not self.heatmap_enabled:
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_intensity",
                                                   "'heatmap_intensity' is only applicable if 'heatmap_enabled' is "
                                                   "True. ")

        if not (isinstance(val, float) or isinstance(val, int)) or not (0 <= val <= 1):
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_intensity",
                                                   "must be a `float` or `int` between 0 and 1. ")

        self._heatmap_intensity = val

    @heatmap_intensity.deleter
    def heatmap_intensity(self):
        """
        Sets 'heatmap_radius' to `None`; VIP will use the default heatmap radius, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'heatmap_radius' has been set to `None`; VIP will use the default heatmap radius, "
                  "if relevant. ")
        self.heatmap_intensity = None

    @property
    def heatmap_radius(self):
        """
        Heatmap radius setting. Must be set to a :class:`float` between 0 and 1. Heatmaps are only applicable for
        geospatial plots. Heatmap radius setting is only applicable if the heatmap_enabled is set to `True`.

        :return: :class:`float`
        """
        return self._heatmap_radius

    @heatmap_radius.setter
    def heatmap_radius(self, val):
        """
        Heatmap radius setting. Must be set to a :class:`float` between 0 and 1. Heatmaps are only applicable for
        geospatial plots. Heatmap radius setting is only applicable if the heatmap_enabled is set to `True`.

        :param val: :class:`float`
        :return: :class:`None`
        """
        if val is None:
            self._heatmap_radius = None
            return

        if not self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_radius",
                                                   "'heatmap_radius' is only applicable for Geospatial plot types. ")

        if not self.heatmap_enabled:
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_radius",
                                                   "'heatmap_radius' is only applicable if 'heatmap_enabled' is True. ")

        if not (isinstance(val, float) or isinstance(val, int)) or not (0 < val):
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_radius",
                                                   "must be a `float` or `int` greater than 0. ")

        self._heatmap_radius = float(val)

    @heatmap_radius.deleter
    def heatmap_radius(self):
        """
        Sets 'heatmap_radius' to `None`; VIP will use the default heatmap radius, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'heatmap_radius' has been set to `None`; VIP will use the default heatmap radius, "
                  "if relevant. ")
        self.heatmap_radius = None

    @property
    def heatmap_radius_unit(self):
        """
        Heatmap radius unit setting. Must be set to a :class:`float` between 0 and 1. Heatmaps are only applicable for
        geospatial plots. Heatmap radius setting is only applicable if the heatmap_enabled is set to `True`.

        :return: :class:`str` and one of {"Kilometers", "Miles", "NauticalMiles"}.
        """
        return self._heatmap_radius_unit

    @heatmap_radius_unit.setter
    def heatmap_radius_unit(self, val):
        """
        Heatmap radius setting. Must be set to a :class:`float` between 0 and 1. Heatmaps are only applicable for
        geospatial plots. Heatmap radius setting is only applicable if the heatmap_enabled is set to `True`.

        :param val: :class:`str` and one of {"Kilometers", "Miles", "NauticalMiles"}.
        :return: :class:`None`
        """
        if val is None:
            self._heatmap_radius_unit = None
            return

        if not self.is_geospatial_plot():
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_radius_unit",
                                                   "'heatmap_radius_unit' is only applicable for Geospatial plot "
                                                   "types.")

        if not self.heatmap_enabled:
            utils.raise_invalid_argument_exception(str(type(val)), "heatmap_radius_unit",
                                                   "'heatmap_radius_unit' is only applicable if 'heatmap_enabled' is "
                                                   "True. ")

        val = utils.case_insensitive_match(utils.HEATMAP_RADIUS_UNITS, val, "heatmap_radius_unit")

        self._heatmap_radius_unit = val

    @heatmap_radius_unit.deleter
    def heatmap_radius_unit(self):
        """
        Sets 'heatmap_radius_unit' to `None`; VIP will use the default heatmap radius unit, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'heatmap_radius_unit' has been set to `None`; VIP will use the default "
                  "heatmap radius unit, if relevant. ")
        self.heatmap_radius_unit = None

    # endregion HeatmapSettings

    # endregion GeospatialSettings
    
    # region HistogramSettings
    
    @property
    def x_bins(self):
        """
        X bins setting. Must be a :class:`int` between 1 and 1000. X bins is only applicable if the 'plot_type' has
        been set to "HISTOGRAM". If there are multiple spatial dimensions (X, Y, Z) mapped, there are additional
        constraints for permissible values.

        :return: :class:`int` between 1 and 1000
        """
        return self._x_bins
    
    @x_bins.setter
    def x_bins(self, val):
        """
        X bins setting. Must be a :class:`int` between 1 and 1000. X bins is only applicable if the 'plot_type' has
        been set to "HISTOGRAM". If there are multiple spatial dimensions (X, Y, Z) mapped, there are additional
        constraints for permissible values.

        :param val: :class:`int` between 1 and 1000
        :return: :class:`None`
        """
        if val is None:
            self._x_bins = None
            return

        if self._plot_type is not "HISTOGRAM":
            utils.raise_invalid_argument_exception(str(type(val)), "x_bins",
                                                   "'x_bins' is only applicable when 'plot_type' is set to "
                                                   "'HISTOGRAM' and a continuous feature has been mapped to 'X'"
                                                   " dimension. ")

        if self.x is None:
            utils.raise_invalid_argument_exception(str(type(val)), "x_bins",
                                                   "'x_bins' is only applicable when 'x' dimension has been mapped. ")

        if not isinstance(val, int) or not (1 <= val <= 1000):
            utils.raise_invalid_argument_exception(str(type(val)), "x_bins",
                                                   "must be `int` and between 1 and 1000. ")

        self._x_bins = val
    
    @x_bins.deleter
    def x_bins(self):
        """
        Sets x bins to `None`; VIP will use the default number of bins for X, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'x_bins' has been set to `None`; VIP will use the default number of x_bins, if relevant")
        self.x_bins = None
    
    @property
    def y_bins(self):
        """
        Y bins setting. Must be a :class:`int` between 1 and 1000. Y bins is only applicable if the 'plot_type' has
        been set to "HISTOGRAM". If there are multiple spatial dimensions (X, Y, Z) mapped, there are additional
        constraints for permissible values.

        :return: :class:`int` between 1 and 1000
        """
        return self._y_bins
    
    @y_bins.setter
    def y_bins(self, val):
        """
        Y bins setting. Must be a :class:`int` between 1 and 1000. Y bins is only applicable if the 'plot_type' has
        been set to "HISTOGRAM". If there are multiple spatial dimensions (X, Y, Z) mapped, there are additional
        constraints for permissible values.

        :param val: :class:`int` between 1 and 1000
        :return: :class:`None`
        """
        if val is None:
            self._y_bins = None
            return

        if self._plot_type is not "HISTOGRAM":
            utils.raise_invalid_argument_exception(str(type(val)), "y_bins",
                                                   "'y_bins' is only applicable when 'plot_type' is set to "
                                                   "'HISTOGRAM' and a continuous feature has been mapped to 'Y'"
                                                   " dimension. ")

        if self.y is None:
            utils.raise_invalid_argument_exception(str(type(val)), "y_bins",
                                                   "'y_bins' is only applicable when 'y' dimension has been mapped. ")

        if not isinstance(val, int) or not (1 <= val <= 1000):
            utils.raise_invalid_argument_exception(str(type(val)), "y_bins",
                                                   "must be `int` and between 1 and 1000. ")

        self._y_bins = val
    
    @y_bins.deleter
    def y_bins(self):
        """
        Sets y bins to `None`; VIP will use the default number of bins for Y, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'y_bins' has been set to `None`; VIP will use the default number of y_bins, if relevant")
        self.y_bins = None

    @property
    def z_bins(self):
        """
        Z bins setting. Must be a :class:`int` between 1 and 1000. Z bins is only applicable if the 'plot_type' has
        been set to "HISTOGRAM". If there are multiple spatial dimensions (X, Y, Z) mapped, there are additional
        constraints for permissible values.

        :return: :class:`int` between 1 and 1000
        """
        return self._z_bins
    
    @z_bins.setter
    def z_bins(self, val):
        """
        Z bins setting. Must be a :class:`int` between 1 and 1000. Z bins is only applicable if the 'plot_type' has
        been set to "HISTOGRAM". If there are multiple spatial dimensions (X, Y, Z) mapped, there are additional
        constraints for permissible values.

        :param val: :class:`int` between 1 and 1000
        :return: :class:`None`
        """
        if val is None:
            self._z_bins = None
            return

        if self._plot_type is not "HISTOGRAM":
            utils.raise_invalid_argument_exception(str(type(val)), "z_bins",
                                                   "'z_bins' is only applicable when 'plot_type' is set to "
                                                   "'HISTOGRAM' and a continuous feature has been mapped to 'Z'"
                                                   " dimension. ")

        if self.z is None:
            utils.raise_invalid_argument_exception(str(type(val)), "z_bins",
                                                   "'z_bins' is only applicable when 'z' dimension has been mapped. ")

        if not isinstance(val, int) or not (1 <= val <= 1000):
            utils.raise_invalid_argument_exception(str(type(val)), "z_bins",
                                                   "must be `int` and between 1 and 1000. ")

        self._z_bins = val
    
    @z_bins.deleter
    def z_bins(self):
        """
        Sets z bins to `None`; VIP will use the default number of bins for Z, if relevant.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'z_bins' has been set to `None`; VIP will use the default number of z_bins, if relevant")
        self.z_bins = None

    @property
    def hist_volume_by(self):
        """
        Histogram volume by setting. Must be set to `str` and match with one of {"count", "avg", "sum", "uniform"}.
        Histogram volume by is only applicable if the 'plot_type' is 'HISTOGRAM'. Default value is 'None' which implies
        VIP will use the default setting for volume by on histogram plots.

        :return: :class:`str`
        """
        return self._hist_volume_by

    @hist_volume_by.setter
    def hist_volume_by(self, val):
        """
        Histogram volume by setting. Must be set to `str` and match with one of {"count", "avg", "sum", "uniform"}.
        Histogram volume by is only applicable if the 'plot_type' is 'HISTOGRAM'. Default value is 'None' which implies
        VIP will use the default setting for volume by on histogram plots.

        :param val: :class:`str` that must match one of {"count", "avg", "sum", "uniform"} or `None`
        :return: :class:`None`
        """
        if val is None:
            self._hist_volume_by = None
            return

        if self._plot_type is not "HISTOGRAM":
            utils.raise_invalid_argument_exception(str(type(val)), "hist_volume_by",
                                                   "'hist_volume_by' is only applicable when 'plot_type' is set to"
                                                   "'HISTOGRAM'")

        self._hist_volume_by = utils.case_insensitive_match(utils.VOLUME_BY_MODES, val, "hist_volume_by")

    @hist_volume_by.deleter
    def hist_volume_by(self):
        """
        Sets the histogram volume by setting to `None`; VIP will use the default setting for volume by on histogram
        plots.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'hist_volume_by' has been set to 'None'; VIP will use the default setting for volume by, "
                  "if relevant. ")
        self.hist_volume_by = None

    # endregion HistogramSettings

    # region LinePlotSettings

    @property
    def viewby(self):
        """
        Line plot view by setting. Must be set to `str` and match with one of {"color", "groupby"}. View by
        is only applicable if the 'plot_type' is 'LINE_PLOT'. Default value is 'None' which implies VIP will
        use the default setting for view by on line plots.

        :return: :class:`str`
        """
        return self._viewby

    @viewby.setter
    def viewby(self, val):
        """
        Line plot view by setting. Must be set to `str` and match with one of {"color", "groupby"}. View by
        is only applicable if the 'plot_type' is 'LINE_PLOT'. Default value is 'None' which implies VIP will
        use the default setting for view by on line plots.

        :param val: :class:`str` that must match one of {"color", "groupby"} or `None`
        :return: :class:`None`
        """
        if val is None:
            self._viewby = None
            return

        if self._plot_type is not "LINE_PLOT":
            utils.raise_invalid_argument_exception(str(type(val)), "viewby",
                                                   "'viewby' is only applicable when 'plot_type' is set to"
                                                   "'LINE_PLOT'")

        self._viewby = utils.case_insensitive_match(utils.VIEWBY_MODES, val, "viewby")

    @viewby.deleter
    def viewby(self):
        """
        Sets the line plot view by setting to `None`; VIP will use the default setting for volume by on line plots.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'viewby' has been set to 'None'; VIP will use the default setting for view by, "
                  "if relevant. ")
        self.viewby = None

    # endregion LinePlotSetting

    # region SurfaceSettings

    @property
    def show_points(self):
        """
        Show points setting. Must be set to a :class:`bool`. Show points is only applicable when 'plot_type'
        is set to one of the surface or line plot types: {"CONFIDENCE_ELLIPSOID", "CONVEX_HULL", "SURFACE", "LINE_PLOT"}

        :return: :class:`bool`
        """
        return self._show_points

    @show_points.setter
    def show_points(self, val):
        """
        Show points setting. Must be set to a :class:`bool`. Show points is only applicable when 'plot_type'
        is set to one of the surface plot types: {"CONFIDENCE_ELLIPSOID", "CONVEX_HULL", "SURFACE", "LINE_PLOT"}

        :param val: :class:`bool`
        :return: :class:`None`
        """
        if val is None:
            # self._show_points = None
            if self._plot_type == "CONFIDENCE_ELLIPSOID":
                self._show_points = "SurfaceAndPoints"
            elif self._plot_type == "CONVEX_HULL":
                self._show_points = "SurfaceAndPoints"
            elif self._plot_type == "SURFACE":
                self._show_points = "SurfaceOnly"
            elif self._plot_type == "LINE_PLOT":
                self._show_points = "SurfaceAndPoints"
            else:
                self._show_points = None
            return

        if self._plot_type not in ["CONFIDENCE_ELLIPSOID", "CONVEX_HULL", "SURFACE", "LINE_PLOT"]:
            utils.raise_invalid_argument_exception(str(type(val)), 'show_points',
                                                   "'show_points' is only applicable on plots with surfaces ("
                                                   "'CONFIDENCE_ELLIPSOID', 'CONVEX_HULL', 'SURFACE', 'LINE_PLOT'). ")

        self._show_points = utils.case_insensitive_match(utils.SURFACE_VIEW_MODES, val, "show_points")

    @show_points.deleter
    def show_points(self):
        """
        Sets 'show_points' to 'None'; VIP will use default setting for point visibility for the specified plot type.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'show_points' has been set to 'None'; VIP will use the default setting for showing points"
                  " with surface plots ('CONFIDENCE_ELLIPSOIDS', 'CONVEX_HULL', 'SURFACE', 'LINE_PLOT'")
        self.show_points = None

    @property
    def confidence(self):
        """
        Confidence setting. Must be set to a :class:`float` and match one of {99.5, 99.0, 97.5, 95.0, 90.0, 80.0,
        75.0, 70.0, 50.0, 30.0, 25.0, 20.0, 10.0, 5.0, 2.5, 1.0, .5}. Show points is only applicable when 'plot_type'
        is "CONFIDENCE_ELLIPSOID". Default is 'None' which implies VIP will use the default confidence interval for
        the Ellipsoid plot.

        :return: :class:`float`
        """
        return self._confidence

    @confidence.setter
    def confidence(self, val):
        """
        Confidence setting. Must be set to a :class:`float` and match one of {99.5, 99.0, 97.5, 95.0, 90.0, 80.0,
        75.0, 70.0, 50.0, 30.0, 25.0, 20.0, 10.0, 5.0, 2.5, 1.0, .5}. Show points is only applicable when 'plot_type'
        is "CONFIDENCE_ELLIPSOID". Default is 'None' which implies VIP will use the default confidence interval for
        the Ellipsoid plot.

        :param val: :class:`float`
        :return: :class:`None`
        """
        if val is None:
            self._confidence = None
            return

        if self._plot_type is not "CONFIDENCE_ELLIPSOID":
            utils.raise_invalid_argument_exception(str(type(val)), "confidence",
                                                   "'confidence' is only applicable when 'plot_type' is set to "
                                                   "'CONFIDENCE_ELLIPSOID'")

        self._confidence = utils.case_insensitive_match(utils.CONFIDENCE_LEVELS, val, "confidence")

    @confidence.deleter
    def confidence(self):
        """
        Sets confidence to 'None'; VIP will use the default confidence interval for the Ellipsoid plot, if relevant.

        :return: :class:`float`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'confidence' has been set to 'None'; VIP will use the default confidence interval for the"
                  " Ellipsoid plot, if relevant. ")
        self.confidence = None

    # endregion SurfaceSettings

    # region Highlights

    @property
    def halo_highlight(self):
        """
        Halo highlight setting. Must be set to a :class:`string` and match one of the values of the feature mapped to
        "halo".

        :return: class:`string` or numeric
        """
        return self._halo_highlight

    @halo_highlight.setter
    def halo_highlight(self, val):
        """
        Halo highlight setting. Must be set to a :class:`string` and match one of the values of the feature mapped to
        "halo".

        :param val: :class:`string` or numeric
        :return: :class:`None`
        """
        if val is None:
            self._halo_highlight = None
            return

        if self._halo is None:
            utils.raise_invalid_argument_exception(str(type(val)), "halo_highlight",
                                                   "'halo_highlight' is only applicable when the 'halo' dimension is "
                                                   "mapped")

        self._halo_highlight = val

    @halo_highlight.deleter
    def halo_highlight(self):
        """
        Sets halo_highlight to 'None'; VIP will use the default highlight value for the feature mapped to on "halo",
        which will be the first value alphabetically.

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'halo_highlight' has been set to 'None'; VIP will use the default value from the feature "
                  "mapped to halo to highlight. ")
        self._halo_highlight = None

    @property
    def pulsation_highlight(self):
        """
        Pulsation highlight setting. Must be set to a :class:`string` and match one of the values of the feature mapped
        to "pulsation".

        :return: class:`string` or numeric
        """
        return self._pulsation_highlight

    @pulsation_highlight.setter
    def pulsation_highlight(self, val):
        """
        Pulsation highlight setting. Must be set to a :class:`string` and match one of the values of the feature mapped
        to"pulsation".

        :param val: :class:`string` or numeric
        :return: :class:`None`
        """
        if val is None:
            self._pulsation_highlight = None
            return

        if self._pulsation is None:
            utils.raise_invalid_argument_exception(str(type(val)), "pulsation_highlight",
                                                   "'pulsation_highlight' is only applicable when the 'pulsation' "
                                                   "dimension is mapped")

        self._pulsation_highlight = val

    @pulsation_highlight.deleter
    def pulsation_highlight(self):
        """
        Sets pulsation_highlight to 'None'; VIP will use the default highlight value for the feature mapped to on
        "pulsation", which will be the first value alphabetically.

        :return:
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'pulsation_highlight' has been set to 'None'; VIP will use the default value from the "
                  "feature mapped to pulsation to highlight. ")
        self._pulsation_highlight = None

    @property
    def playback_highlight(self):
        """
        Playback highlight setting. Must be set to a :class:`string` and match one of the values of the feature mapped
        to "playback".

        :return: class:`string` or numeric
        """
        return self._playback_highlight

    @playback_highlight.setter
    def playback_highlight(self, val):
        """
        Playback highlight setting. Must be set to a :class:`string` and match one of the values of the feature mapped
        to "playback".

        :param val: :class:`string` or numeric
        :return: :class:`None`
        """
        if val is None:
            self._playback_highlight = None
            return

        if self._playback is None:
            utils.raise_invalid_argument_exception(str(type(val)), "playback_highlight",
                                                   "'playback_highlight' is only applicable when the 'playback' "
                                                   "dimension is mapped")

        self._playback_highlight = val

    @playback_highlight.deleter
    def playback_highlight(self):
        """
        Sets playback_highlight to 'None'; VIP will use the default highlight value for the feature mapped to on
        "playback", which will be "Show All".

        :return: :class:`None`
        """
        if self.log_level >= api.LOG_HELP_LEVEL:
            print("Attribute 'playback_highlight' has been set to 'None'; VIP will use the default value from the "
                  "feature mapped to playback to highlight. ")
        self._playback_highlight = None

    # endregion Highlights

    # endregion PlotSettings
