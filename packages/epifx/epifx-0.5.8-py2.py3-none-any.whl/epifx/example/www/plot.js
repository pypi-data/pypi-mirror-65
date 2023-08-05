/**
 * Produce animated plots.
 *
 * The structure of each plot object is:
 *
 *     plot
 *      + cfg (see Plot.default_config and Plot.peak_config)
 *      + slider (input element, forecast plot only)
 *      + slider_prev (button element, forecast plot only)
 *      + slider_next (button element, forecast plot only)
 *      + svg  (root SVG element)
 *      + span_id (ID string of the element to contain the plot)
 *      + contents (group element that contains every plot component)
 *      + moveto() (update the plot when the slider position changes)
 *      + fs_date (the current forecast date)
 *      + df (plot data)
 *      + peak_df (plot data, forecast plot only)
 *      + obs (plot data, forecast plot only)
 *      + upper (plot data, forecast plot only)
 *      + locn (name of the forecast location)
 *      + scale
 *         + x (d3 scale object for the x-axis)
 *         + y (d3 scale object for the y-axis)
 *      + axis
 *         + coords (coordinate bounds in the SVG)
 *         + x (d3 scale object for the x-axis)
 *         + x_bot (line for the bottom x-axis)
 *         + x_label (svg:text element for x-axis label)
 *         + y (d3 scale object for the y-axis)
 *         + y_left (line for the left y-axis)
 *         + y_label (svg:text element for y-axis label)
 *      + draw
 *         + obsline() (draw a line, y = value)
 *         + maxline() (draw a line, y = ymin)
 *         + minline() (draw a line, y = ymax)
 *         + area() (draw a shaded area from ymin to ymax)
 *      + series (data elements, indexed by CI)
 *         + 0 (contains SVG paths for the median data)
 *         + 50 (contains SVG paths for the 50% CI data)
 *         + 95 (contains SVG paths for the 95% CI data)
 *      + update() (redraw the plot)
 *
 * To-do list:
 *
 *     (a) Store the initial and current sizing configuration separately.
 *
 *     (b) Separate creating plot elements from setting position and size.
 *
 */

/* Directives for JSHint (http://jshint.com/) */
/* jshint esversion: 6 */
/* global d3 */

/**
 * Create a new namespace to contain all of the variables and functions.
 */
var Plot = Plot || {};

/**
 * Pre-defined plot axis templates.
 */

// A standard linear numerical axis, with adjustable precision.
Plot.num_axis = function(label, precision) {
    "use strict";
    return {
        scale: function() { return d3.scale.linear(); },
        tick: 4,
        grid: 8,
        fmt_tick: function(d) { return d.toFixed(precision); },
        label: label
    };
};

// A date axis.
Plot.date_axis = function(label) {
    "use strict";
    return {
        scale: function() { return d3.time.scale(); },
        tick: 8,
        grid: 8,
        fmt_tick: d3.time.format("%-d %b"),
        label: label
    };
};

// A time axis, where the underlying data is in seconds and is displayed as
// MM:SS. Note that hours are not accounted for, the minutes simply increase.
Plot.time_axis = function(label) {
    "use strict";
    return {
        scale: function() { return d3.scale.linear(); },
        tick: 4,
        grid: 8,
        fmt_tick: function(secs) {
            var mins = Math.floor(secs / 60);
            secs = Math.round(secs - 60 * mins);
            if (secs < 10) {
                return mins + ":0" + secs;
            } else {
                return mins + ":" + secs;
            }
        },
        label: label
    };
};

/**
 * Adjust the size and position of all plot elements.
 */
Plot.resize = function() {
    "use strict";
    var w = document.getElementById("content").offsetWidth * 0.6;
    var h = document.getElementById("content").offsetHeight;
    var small = false;

    if (w <= 480) {
        w = document.getElementById("content").offsetWidth;
        small = true;
    }
    h = Math.min(0.75 * w,
                 0.90 * document.documentElement.clientHeight);

    Plot.created_plots.forEach(function(plot) {
        plot.cfg.dims.w = w;
        plot.cfg.dims.h = h;

        if (small) {
            plot.cfg.x.tick = plot.cfg.x.grid / 2;
            plot.cfg.y.tick = plot.cfg.y.grid / 2;
        } else {
            plot.cfg.x.tick = plot.cfg.x.grid;
            plot.cfg.y.tick = plot.cfg.y.grid;
        }

        plot.svg
            .attr("width", w)
            .attr("height", h)
            .attr("preserveAspectRatio", "none");

        var translate_x = plot.cfg.dims.margin_pcnt * w;
        var translate_y = (1 - plot.cfg.dims.margin_pcnt) * h;
        var scale_x = 1 - 2 * plot.cfg.dims.margin_pcnt;
        var scale_y = 2 * plot.cfg.dims.margin_pcnt - 1;

        plot.contents.attr("transform",
                           "matrix(" + scale_x  + ",0,0," + scale_y + "," +
                           translate_x + "," + translate_y + ")");

        // Update the axes.
        Plot.make_axes(plot, plot.df.lims);

        // Re-position the plot title.
        Plot.posn_text(plot.contents.title,
                       0.5 * (plot.axis.coords.x0 + plot.axis.coords.x1),
                       plot.axis.coords.y1);

        // Redraw the plot contents.
        plot.update();
    });
};

/**
 *
 */
Plot.make_svg = function(cfg, span_id) {
    "use strict";
    // Create a new namespace to contain the plot.
    var plot = { cfg: cfg };

    // Create the slider bar for navigating forecasts by date.
    if (cfg.plot_type == "fs") {
        var slider_div = d3.select(span_id)
            .append("div");
        plot.slider = slider_div
            .attr("class", "slider")
            .append("input");
        plot.slider
            .attr("class", "slider")
            .attr("id", "fs_slider")
            .attr("type", "range")
            .attr("min", 0)
            .attr("max", 0)
            .attr("step", 1);

        // Create buttons for stepping forward/backward.
        var button_div = slider_div.append("div");
        button_div.attr("class", "buttons");
        plot.slider_prev = button_div.append("button");
        plot.slider_prev
            .attr("type", "button")
            .attr("data-step", "-1")
            .attr("class", "prev")
            .text("Prev");
        plot.slider_next = button_div.append("button");
        plot.slider_next
            .attr("type", "button")
            .attr("data-step", "1")
            .attr("class", "next")
            .text("Next");
        plot.slider_prev.on("click", function() {
            plot.slider[0][0].stepDown();
            var ev_change = new Event("change");
            var ev_input = new Event("input");
            plot.slider[0][0].dispatchEvent(ev_input);
            plot.slider[0][0].dispatchEvent(ev_change);
        });
        plot.slider_next.on("click", function() {
            plot.slider[0][0].stepUp();
            var ev_change = new Event("change");
            var ev_input = new Event("input");
            plot.slider[0][0].dispatchEvent(ev_input);
            plot.slider[0][0].dispatchEvent(ev_change);
        });
    }

    // Create the SVG element that will contain the plot.
    plot.svg = d3.select(span_id)
        .append("svg:svg")
        .attr("width", parseFloat(cfg.dims.w))
        .attr("height", parseFloat(cfg.dims.h))
        .attr("preserveAspectRatio", "none");
    plot.span_id = span_id;

    // Note that the CSS box model considers both padding (inner) and margins
    // (outer) to be in *addition* to the content area, so we should probably
    // respect that here, rather than considering the padding as internal and
    // being accounted for by the axis scales.
    var translate_x = cfg.dims.margin_pcnt * parseFloat(cfg.dims.w);
    var translate_y = (1 - cfg.dims.margin_pcnt) * parseFloat(cfg.dims.h);
    var scale_x = 1 - 2 * cfg.dims.margin_pcnt;
    var scale_y = 2 * cfg.dims.margin_pcnt - 1;

    // Create the group element that will contain every plot component.
    plot.contents = plot.svg.append("svg:g")
        .attr("transform",
              "matrix(" + scale_x  + ",0,0," + scale_y + "," +
              translate_x + "," + translate_y + ")");

    return plot;
};

/**
 *
 */
Plot.posn_text = function(elt, x, y, angle) {
    "use strict";
    var fnx, fny;
    if (typeof x !== "function") {
        fnx = function(d) { return x; };
    } else {
        fnx = x;
    }
    if (typeof y !== "function") {
        fny = function(d) { return y; };
    } else {
        fny = y;
    }
    if (angle === undefined) {
        angle = "";
    } else {
        angle = "rotate(" + angle + ")";
    }
    return elt.attr("x", x).attr("y", y)
        .attr("transform", function(d) {
            return "translate(" + fnx(d) + "," + fny(d) + ") " +
                "scale(1, -1) " + angle + " translate(" +
                (0 - fnx(d)) + "," + (0 - fny(d)) + ")";
        });
};

Plot.append_text = function(elt, x, y, text, angle) {
    "use strict";
    return Plot.posn_text(elt.append("svg:text").text(text), x, y, angle);
};

/**
 *
 */
Plot.make_axes = function(plot, lims) {
    "use strict";
    // Important: create new scale objects so we can adjust their domains
    // without affecting other plots.
    // Note: it might be preferable to ensure a uniform vertical scale across
    // all plots.
    if (plot.scale === undefined) {
        plot.scale = {};
        plot.scale.x = plot.cfg.x.scale();
        plot.scale.y = plot.cfg.y.scale();
    }

    plot.axis = plot.axis || {};
    plot.axis.x = plot.scale.x.domain([lims.x0, lims.x1])
        .range([plot.cfg.dims.padding_x,
                plot.cfg.dims.w - plot.cfg.dims.padding_x]);
    plot.axis.y = plot.scale.y.domain([lims.y0, lims.y1])
        .range([plot.cfg.dims.padding_y,
                plot.cfg.dims.h - plot.cfg.dims.padding_y]);

    // Determine the coordinate bounds.
    plot.axis.coords = {
        x0: plot.axis.x(lims.x0),
        x1: plot.axis.x(lims.x1),
        y0: plot.axis.y(lims.y0),
        y1: plot.axis.y(lims.y1)
    };
    // Convenience variable for the axis-drawing functions.
    var clims = plot.axis.coords;

    // Draw the bottom x-axis.
    if (plot.axis.x_bot === undefined) {
        plot.axis.x_bot = plot.contents.append("svg:line");
    }
    plot.axis.x_bot
        .attr("x1", clims.x0)
        .attr("y1", clims.y0)
        .attr("x2", clims.x1)
        .attr("y2", clims.y0);
    // Draw the left y-axis.
    if (plot.axis.y_left === undefined) {
        plot.axis.y_left = plot.contents.append("svg:line");
    }
    plot.axis.y_left
        .attr("x1", clims.x0)
        .attr("y1", clims.y0)
        .attr("x2", clims.x0)
        .attr("y2", clims.y1);
    // Draw the top and right axes, if specified.
    if (plot.cfg.draw_box) {
        if (plot.axis.x_top === undefined) {
            plot.axis.x_top = plot.contents.append("svg:line");
        }
        plot.axis.x_top
            .attr("x1", clims.x0)
            .attr("y1", clims.y1)
            .attr("x2", clims.x1)
            .attr("y2", clims.y1);
        if (plot.axis.y_right === undefined) {
            plot.axis.y_right = plot.contents.append("svg:line");
        }
        plot.axis.y_right
            .attr("x1", clims.x1)
            .attr("y1", clims.y0)
            .attr("x2", clims.x1)
            .attr("y2", clims.y1);
    }

    // Draw the x-axis label.
    if (plot.axis.x_label === undefined) {
        plot.axis.x_label = Plot.append_text(plot.contents,
                                             plot.cfg.dims.w / 2,
                                             0,
                                             plot.cfg.x.label)
            .attr("class", "xLabel")
            .style("text-anchor", "middle");
    } else {
        // Re-position the x-axis label.
        Plot.posn_text(plot.axis.x_label, plot.cfg.dims.w / 2, 0);
    }

    // Draw the y-axis label.
    if (plot.axis.y_label === undefined) {
        plot.axis.y_label = Plot.append_text(plot.contents,
                                             0,
                                             plot.cfg.dims.h / 2,
                                             plot.cfg.y.label,
                                             -90)
            .attr("dy", "0.5em")
            .attr("class", "yLabel")
            .style("text-anchor", "middle");
    } else {
        // Re-position the x-axis label.
        Plot.posn_text(plot.axis.y_label, 0, plot.cfg.dims.h / 2, -90);
    }

    plot.contents.selectAll(".xTickLabel").remove();
    plot.contents.selectAll(".yTickLabel").remove();
    plot.contents.selectAll(".xTick").remove();
    plot.contents.selectAll(".yTick").remove();
    plot.contents.selectAll(".xGrid").remove();
    plot.contents.selectAll(".yGrid").remove();

    // Draw the x-axis tick labels.
    Plot.posn_text(plot.contents.selectAll(".xTickLabel")
                   .data(plot.axis.x.ticks(plot.cfg.x.tick))
                   .enter().append("svg:text"),
                   function(d) { return plot.axis.x(d); },
                   0.5 * plot.cfg.dims.padding_y)
        .attr("class", "xTickLabel")
        .text(plot.cfg.x.fmt_tick)
        .attr("text-anchor", "middle");

    // Draw the y-axis tick labels.
    Plot.posn_text(plot.contents.selectAll(".yTickLabel")
                   .data(plot.axis.y.ticks(plot.cfg.y.tick))
                   .enter().append("svg:text"),
                   clims.x0 * 42 / 50,
                   function(d) { return plot.axis.y(d); })
        .attr("class", "yTickLabel")
        .text(plot.cfg.y.fmt_tick)
        .attr("text-anchor", "end")
        .attr("dy", 4);

    // Draw the x-axis tick lines.
    plot.contents.selectAll(".xTick")
        .data(plot.axis.x.ticks(plot.cfg.x.tick))
        .enter().append("svg:line")
        .attr("class", "xTick")
        .attr("x1", function(d) { return plot.axis.x(d); })
        .attr("y1", clims.y0)
        .attr("x2", function(d) { return plot.axis.x(d); })
        /* Scale the size of the ticks relative to the y domain. */
        .attr("y2", clims.y0 * 42 / 50);

    // Draw the y-axis tick lines.
    plot.contents.selectAll(".yTick")
        .data(plot.axis.y.ticks(plot.cfg.y.tick))
        .enter().append("svg:line")
        .attr("class", "yTick")
        .attr("y1", function(d) { return plot.axis.y(d); })
        /* Scale the size of the ticks relative to the x domain. */
        .attr("x1", clims.x0 * 45 / 50)
        .attr("y2", function(d) { return plot.axis.y(d); })
        .attr("x2", clims.x0);

    // Plot the vertical grid lines.
    plot.contents.selectAll(".xGrid")
        .data(plot.axis.x.ticks(plot.cfg.x.grid))
        .enter().append("svg:line")
        .attr("class", "grid xGrid")
        .attr("x1", function(d) { return plot.axis.x(d); })
        .attr("y1", clims.y0)
        .attr("x2", function(d) { return plot.axis.x(d); })
        .attr("y2", clims.y1);

    // Plot the horizontal grid lines.
    plot.contents.selectAll(".yGrid")
        .data(plot.axis.y.ticks(plot.cfg.y.grid))
        .enter().append("svg:line")
        .attr("class", "grid yGrid")
        .attr("y1", function(d) { return plot.axis.y(d); })
        .attr("x1", clims.x0)
        .attr("y2", function(d) { return plot.axis.y(d); })
        .attr("x2", clims.x1);
};

/**
 *
 */
Plot.connect_slider = function(plot) {
    "use strict";
    plot.moveto = function() {
        // Plot the selected forecast, if the slider position has changed.
        if (plot.df.fs_counter != plot.slider[0][0].value) {
            plot.df.fs_counter = plot.slider[0][0].value;
            plot.update();
        }
    };

    // Connect the slider events.
    plot.slider.on("input.self", plot.moveto);
    plot.slider.on("change.self", plot.moveto);
};

Plot.link_to_other_slider = function(src, dest) {
    "use strict";
    dest.moveto = function() {
        // Update when the slider position has changed.
        dest.fs_date = src.df.fs_dates[src.slider[0][0].value];
        if (dest.update !== undefined) {
            dest.update();
        }
    };

    // Connect the slider events.
    src.slider.on("input.link", dest.moveto);
    src.slider.on("change.link", dest.moveto);
};

/**
 *
 */
Plot.prepare_data = function(plot, data) {
    "use strict";
    // Use UTC time to avoid changes in date due to TZ conversions.
    var parseDate = d3.time.format.utc("%Y-%m-%d").parse;
    plot.df = {};
    plot.locn = data.location_name;
    var om_span = d3.select("#obs_model");
    var om_value;
    if (! om_span.empty() && data.obs_model !== undefined) {
        // Descriptive names for known observation model parameters.
        var om_names = {
            bg_frac: "Background fraction",
            k_denom: "Denominator scale",
            k_obs: "Observation scale",
            bg_obs: "Background rate",
            pr_obs: "Observation probability",
            disp: "Dispersion"};
        var om_html = "";
        Object.keys(data.obs_model).forEach(function(name, index) {
            if (index > 0) {
                om_html = om_html + "\n<br/>";
            }
            // Round to 8 decimal places, then discard trailing zeros.
            om_value = +parseFloat(data.obs_model[name]).toFixed(8);
            if (name in om_names) {
                om_html = om_html + om_names[name] + ": " + om_value;
            } else {
                om_html = om_html + name + ": " + om_value;
            }
        });
        om_span.html(om_html);
    }

    // Determine the range of observed values and the observed peak timing.
    var obs_keys = Object.keys(data.obs);
    var max_val = 0;
    var min_val = 1e6;
    var peak_date = parseDate(data.obs[obs_keys[0]][0].date);
    var first_obs = peak_date;
    var last_obs = peak_date;

    var fs_date;

    data.upper = {};
    obs_keys.forEach(function(at_d) {
        data.obs[at_d].forEach(function(d) {
            d.date = parseDate(d.date);
            d.value = +d.value;
            if (d.incomplete === undefined) {
                d.incomplete = false;
            }
            if (d.value > max_val) { peak_date = d.date; }
            max_val = Math.max(max_val, d.value);
            min_val = Math.min(min_val, d.value);
            if (d.date < first_obs) { first_obs = d.date; }
            if (d.date > last_obs) { last_obs = d.date; }
        });
        data.upper[at_d] = data.obs[at_d].filter(function(d) {
            return d.incomplete && d.upper_bound !== undefined &&
                d.upper_bound > 0;
        });
    });

    var ix = window.location.href.indexOf("?");
    var query;
    if (ix > 0) {
        query = window.location.href.slice(
            window.location.href.indexOf("?") + 1);
    }

    var min_date, max_date, cint, cdata;

    if (plot.cfg.plot_type == "fs") {
        //
        // Prepare the weekly forecasting data.
        //

        plot.df.fs_dates = Object.keys(data.forecasts);

        // Ensure that the estimation run is not included.
        var last_fs = new Date(plot.df.fs_dates[plot.df.fs_dates.length - 1]);
        // Note: getMonth() returns [0, 11], getDate() returns [1, 31].
        var end_of_year = last_fs.getMonth() == 11 && last_fs.getDate() == 31;
        if (end_of_year) {
            plot.df.fs_dates.splice(plot.df.fs_dates.length - 1, 1);
        }

        plot.slider.attr("max", plot.df.fs_dates.length - 1);
        // Allow the forecast date to be specified in the query string.
        if (ix > 0) {
            var counter = 0;
            for (fs_date of plot.df.fs_dates) {
                if (fs_date === query) {
                    plot.df.fs_counter = counter;
                    break;
                }
                counter++;
            }
        }

        if (plot.df.fs_counter === undefined) {
            if (plot.cfg.most_recent_first) {
                // Start by displaying the latest forecast.
                plot.df.fs_counter = plot.df.fs_dates.length - 1;
            } else {
                // Start by displaying the earliest forecast.
                plot.df.fs_counter = 0;
            }
        }
        plot.slider[0][0].value = plot.df.fs_counter;
        var ev_change = new Event("change");
        var ev_input = new Event("input");
        plot.slider[0][0].dispatchEvent(ev_input);
        plot.slider[0][0].dispatchEvent(ev_change);

        // Set the lower bound for the x-axis domain; use the maximum of the
        // first observation and March 1st.
        min_date = new Date(peak_date.getFullYear() + "-03-01");
        if (first_obs > min_date) {
            min_date = first_obs;
        }

        // Set the upper bound for the x-axis domain; use the maximum of the
        // last observation and October 31st.
        max_date = new Date(peak_date.getFullYear() + "-10-31");
        if (last_obs > max_date) {
            max_date = last_obs;
        }

        var date_ok = function(d) {
            return d.date >= min_date && d.date <= max_date;
        };

        var date_after_fs = function(fs_as_date) {
            return function(d) {
                return d.date > fs_as_date && d.date <= max_date;
            };
        };

        var update_y_bounds = function(d) {
            d.date = parseDate(d.date);
            d.ymin = +d.ymin;
            d.ymax = +d.ymax;
            max_val = Math.max(max_val, d.ymax);
            min_val = Math.min(min_val, d.ymin);
        };

        // Load the forecasts for each forecasting date.
        plot.peak_df = {};
        plot.obs = {};
        plot.upper = {};
        var num_fs = plot.df.fs_dates.length;
        for (fs_date of plot.df.fs_dates) {
            var fs_as_date = new Date(fs_date);
            plot.df[fs_date] = {};
            plot.peak_df[fs_date] = {};
            plot.obs[fs_date] = data.obs[fs_date].filter(date_ok);
            plot.upper[fs_date] =  data.upper[fs_date].filter(date_ok);

            var future_obs = data.obs[plot.df.fs_dates[num_fs - 1]]
                .filter(date_after_fs(fs_as_date)).slice();
            Array.prototype.push.apply(plot.obs[fs_date], future_obs.slice());
            for (cint of Object.keys(data.forecasts[fs_date])) {
                cdata = data.forecasts[fs_date][cint];
                cdata.forEach(update_y_bounds);
                // Stop plotting forecast outputs at the end of November.
                plot.df[fs_date][cint] = cdata.filter(date_ok);
                // Determine when the ymin and ymax curves peak.
                var ymin_peak = cdata.reduce(function(prev, curr, ix, array) {
                    if (curr.ymin > prev.ymin) {
                        return curr;
                    } else {
                        return prev;
                    }
                });
                var ymax_peak = cdata.reduce(function(prev, curr, ix, array) {
                    if (curr.ymax > prev.ymax) {
                        return curr;
                    } else {
                        return prev;
                    }
                });
                // Record the time and size of each peak.
                plot.peak_df[fs_date][cint] = [
                    [ymin_peak.date, ymin_peak.ymin, -1],
                    [ymax_peak.date, ymax_peak.ymax, 1]];
            }
        }

        // Enforce an upper bound on the y-axis, if provided.
        if (plot.cfg.y.upper_bound !== undefined) {
            max_val = plot.cfg.y.upper_bound;
        }

        // Apply location-specific units and labels.
        plot.cfg.y.label = data.obs_axis_lbl;
        plot.cfg.y.tip_lbl = data.obs_datum_lbl;
        plot.cfg.y.fmt_tick = function(d) {
            return d.toFixed(data.obs_axis_prec);
        };
        plot.cfg.y.tip_fmt = function (d) {
            return d.toFixed(data.obs_datum_prec);
        };

        // Determine the data bounds.
        plot.df.lims = {
            x0: min_date,
            x1: max_date,
            y0: 0, // Enforce a lower bound of zero.
            y1: max_val * 1.05
        };
    } else if (plot.cfg.plot_type == "peak") {
        //
        // Prepare the predicted peak timing data.
        //

        plot.df.truth = peak_date;

        // Only consider forecasting dates up to the true peak.
        plot.df.fs_dates = Object.keys(data.timing);

        // Allow the forecast date to be specified in the query string.
        if (ix > 0) {
            for (fs_date of plot.df.fs_dates) {
                if (fs_date === query) {
                    plot.fs_date = fs_date;
                    break;
                }
            }
        }

        min_date = parseDate(plot.df.fs_dates[0]);
        max_date = parseDate(plot.df.fs_dates[plot.df.fs_dates.length - 1]);

        var update_bounds = function(cint, fs_date) {
            return function(d) {
                d.date = parseDate(fs_date);
                d.ymin = parseDate(d.ymin);
                if (d.ymax == "2016-01-01") { d.ymax = "2015-12-31"; }
                d.ymax = parseDate(d.ymax);
                d.truth = peak_date;
                plot.df[cint].push(d);
                max_date = new Date(Math.max(max_date, d.ymax));
                min_date = new Date(Math.min(min_date, d.ymin));
            };
        };

        plot.df.cints = [0, 50, 95];
        for (cint of plot.df.cints) {
            plot.df[cint] = [];
            for (fs_date of plot.df.fs_dates) {
                cdata = data.timing[fs_date][cint];
                cdata.forEach(update_bounds(cint, fs_date));
            }
        }

        // Ignore peak timing forecasts where the widest credible interval has
        // zero width and predicts the peak will occur on the forecasting date
        // (i.e., where the peak has already passed and all forecasts are
        // monotonically decreasing).
        var last_ix = plot.df[95].length - 1;
        var last_ci = plot.df[95][last_ix];
        var pk_now = last_ci.ymin.getTime() === last_ci.ymax.getTime() &&
            last_ci.ymin.getTime() === last_ci.date.getTime();
        while (pk_now) {
            for (cint of plot.df.cints) {
                plot.df[cint].pop();
            }
            last_ix = last_ix - 1;
            if (last_ix < 0) {
                break;
            }
            last_ci = plot.df[95][last_ix];
            pk_now = last_ci.ymin.getTime() === last_ci.ymax.getTime() &&
                last_ci.ymin.getTime() === last_ci.date.getTime();
        }

        // Determine the data bounds.
        plot.df.lims = {
            x0: parseDate(plot.df.fs_dates[0]),
            x1: parseDate(plot.df.fs_dates[plot.df.fs_dates.length - 1]),
            y0: min_date,
            y1: max_date
        };
    } else {
        console.log("ERROR: unknown plot type '" + plot.cfg.plot_type + "'");
    }
};

/**
 * Allow all plots to share common axis scales.
 */
Plot._common_scales = false;

Plot.common_scales = function(enable) {
    "use strict";
    if (enable === undefined) {
        return Plot._common_scales;
    } else {
        Plot._common_scales = enable;
    }
};

/**
 * Calculate the common axis limits and apply them to all plots.
 */
Plot.update_axes = function(span_id, lims) {
    "use strict";
    var glims = Object.create(lims);
    Plot.created_plots.forEach(function(p) {
        if (p.span_id !== span_id) {
            if (p.df !== undefined && p.df.lims !== undefined) {
                glims.x0 = Math.min(glims.x0, p.df.lims.x0);
                glims.x1 = Math.max(glims.x1, p.df.lims.x1);
                glims.y0 = Math.min(glims.y0, p.df.lims.y0);
                glims.y1 = Math.max(glims.y1, p.df.lims.y1);
            }
        }
    });
    glims.x0 = new Date(glims.x0);
    glims.x1 = new Date(glims.x1);
    Plot.global_lims = glims;

    Plot.created_plots.forEach(function(p) {
        Plot.make_axes(p, Plot.global_lims, false);
        if (p.update !== undefined) {
            p.update(false);
        }
    });
};

/**
 * Add or subtract a number of days from a Date object.
 */
Plot.add_days = function(date, days) {
    "use strict";
    return new Date(date.valueOf() + days * 86400000);
};

/**
 *
 */
Plot.loader = function(plot) {
    "use strict";
    return function(error, data) {
        if (error !== null) {
            console.log(error);
            return;
        }

        // Load the data into plot.df.
        Plot.prepare_data(plot, data);

        if (Plot.common_scales()) {
            // Apply global axis limits to all plots (including this one).
            Plot.update_axes(plot.span_id, plot.df.lims);
        } else {
            // Create the (plot-specific) axis scales.
            Plot.make_axes(plot, plot.df.lims, false);
        }

        // Avoid re-creating this when loading a new set of forecasts.
        if (plot.contents.title === undefined) {
            plot.contents.title = Plot.append_text(
                plot.contents,
                0.5 * (plot.axis.coords.x0 + plot.axis.coords.x1),
                plot.axis.coords.y1, "")
                .attr("class", "plotTitle")
                .attr("dy", "-0.5em")
                .attr("text-anchor", "middle");
        }

        // How to construct lines from a data series.
        if (plot.draw === undefined) {
            plot.draw = {};
            plot.draw.obsline = d3.svg.line()
                .x(function(d) { return plot.axis.x(d.date); })
                .y(function(d) { return plot.axis.y(d.value); });
            plot.draw.maxline = d3.svg.line()
                .x(function(d) { return plot.axis.x(d.date); })
                .y(function(d) { return plot.axis.y(d.ymax); });
            plot.draw.minline = d3.svg.line()
                .x(function(d) { return plot.axis.x(d.date); })
                .y(function(d) { return plot.axis.y(d.ymin); });
            // How to construct highlighted regions from a data series.
            plot.draw.area = d3.svg.area()
                .x(function(d) { return plot.axis.x(d.date); })
                .y0(function(d) { return plot.axis.y(d.ymin); })
                .y1(function(d) { return plot.axis.y(d.ymax); });
        }

        if (plot.series === undefined) {
            plot.series = {};
        }

        // For variable speed and better loop control see:
        // http://stackoverflow.com/questions/1280263/changing-the-interval-of-setinterval-while-its-running

        plot.update = function() {
            var date_str = function(d) {
                var month_names = ["January", "February", "March", "April",
                                   "May", "June", "July", "August",
                                   "September", "October", "November",
                                   "December"];
                return month_names[d.getMonth()] + " " + d.getDate() +
                    ", " + d.getFullYear();
            };

            var c_class = {"0": "data-md", "50": "data-50", "95": "data-95"};
            var cint, c_data, fs_as_date;
            var p = "svg:path";

            var get_x_d0 = function(d) { return plot.axis.x(d[0]); };
            var get_y_d1 = function(d) { return plot.axis.y(d[1]); };

            var cint_lbl = function(cint) {
                return function(d) {
                    var cint_lbl = "Median";
                    if (cint > 0) {
                        cint_lbl = cint + "% CI";
                        if (d[2] > 0) {
                            cint_lbl = cint_lbl + " upper";
                        } else {
                            cint_lbl = cint_lbl + " lower";
                        }
                    }
                    return cint_lbl + " peak: " + date_str(d[0]) +
                        " (" + plot.cfg.y.tip_fmt(d[1]) + " " +
                        plot.cfg.y.tip_lbl + ")";
                };
            };

            if (plot.cfg.plot_type == "fs") {
                //
                // Plot the weekly forecasting data.
                //

                var fs_date = plot.df.fs_dates[plot.df.fs_counter];
                fs_as_date = new Date(fs_date);
                var fs_title = date_str(fs_as_date);
                plot.contents.title.text("Forecast for " + plot.locn +
                                         " at " + fs_title);

                var fs_ints = plot.df[fs_date];
                var fs_keys = Object.keys(fs_ints).reverse();

                for (cint of fs_keys) {
                    c_data = plot.df[fs_date][cint].slice().reverse();

                    if (plot.series[cint] === undefined) {
                        plot.series[cint] = {};
                        plot.series[cint].area = plot.contents.append(p);
                        plot.series[cint].lmin = plot.contents.append(p);
                        plot.series[cint].lmax = plot.contents.append(p);
                        plot.series[cint].area
                            .style("opacity", 0);
                    }

                    // Fade out the previously-highlighted regions, if any.
                    plot.series[cint].area
                        .transition().duration(200)
                        .style("opacity", 0);
                    // Update the regions and then fade them back in.
                    plot.series[cint].area.data([c_data])
                        .transition().delay(200).duration(100)
                        .attr("class", "area " + c_class[cint])
                        .attr("d", plot.draw.area)
                        .transition().duration(200)
                        .style("opacity", 1.0);

                    // Transition from the previous lower bounds to the new.
                    plot.series[cint].lmin.data([c_data])
                        .transition().duration(500)
                        .attr("class", "series " + c_class[cint])
                        .attr("d", plot.draw.minline);
                    // Transition from the previous upper bounds to the new.
                    plot.series[cint].lmax.data([c_data])
                        .transition().duration(500)
                        .attr("class", "series " + c_class[cint])
                        .attr("d", plot.draw.maxline);
                }

                for (cint of fs_keys) {
                    var pk_data = plot.peak_df[fs_date][cint];

                    if (plot.series[cint].peaks === undefined) {
                        // Create a group to contain the peak points.
                        plot.series[cint].peaks = plot.contents.append(
                            "svg:g");
                    } else {
                        // Remove the previous peak points.
                        plot.series[cint].peaks.selectAll("circle").remove();
                    }

                    // Draw a point for each credible interval peak.
                    plot.series[cint].peaks.selectAll("circle")
                        .data(pk_data)
                        .enter().append("svg:circle")
                        .attr("r", 7)
                        .attr("cx", get_x_d0)
                        .attr("cy", get_y_d1)
                        .attr("class", "series area  " + c_class[cint])
                        // Add a mouse-over title to identify each peak.
                        .append("svg:title")
                        .text(cint_lbl(cint));
                }

                // Remove all upper bound markings.
                plot.contents.selectAll(".upper").remove();
                // Create new upper bound markings.
                plot.contents.selectAll(".upper")
                    .data(plot.upper[fs_date])
                    .enter()
                    .append("svg:line")
                    .attr("class", "upper data-rw incomplete")
                    .attr("x1", function(d) {
                        return plot.axis.x(Plot.add_days(d.date, 2)); })
                    .attr("x2", function(d) {
                        return plot.axis.x(Plot.add_days(d.date, -2)); })
                    .attr("y1", function(d) {
                        return plot.axis.y(d.upper_bound); })
                    .attr("y2", function(d) {
                        return plot.axis.y(d.upper_bound); })
                    // Add a mouse-over title to identify upper bounds.
                    .append("svg:title")
                    .text(function(d) {
                        return "Upper bound: " +
                            plot.cfg.y.tip_fmt(d.upper_bound) +
                            " " + plot.cfg.y.tip_lbl + " by " +
                            date_str(d.date);
                    });

                // Remove all data points.
                plot.contents.selectAll(".dot").remove();
                // Create new data points.
                plot.contents.selectAll(".dot")
                    .data(plot.obs[fs_date])
                    .enter()
                    .append("svg:circle")
                    .attr("class", function(d) {
                        if (d.date > fs_as_date) {
                            return "dot data-rw future";
                        } else if (d.incomplete) {
                            return "dot data-rw incomplete";
                        } else {
                            return "dot data-rw";
                        }
                    })
                    .attr("r", function(d) {
                        if (d.date > fs_as_date) {
                            return 4.5;
                        } else {
                            return 5.0;
                        }
                    })
                    .attr("cx", function(d) { return plot.axis.x(d.date); })
                    .attr("cy", function(d) { return plot.axis.y(d.value); })
                    // Add a mouse-over title to identify future observations.
                    .append("svg:title")
                    .text(function(d) {
                        var prefix = "Data: ";
                        var value_str = plot.cfg.y.tip_fmt(d.value);
                        if (d.incomplete) {
                            prefix = "Incomplete data: ";
                            if (d.upper_bound === undefined ||
                                d.upper_bound === 0) {
                                value_str = 'at least ' + value_str;
                            } else {
                                value_str = value_str + " - " +
                                    plot.cfg.y.tip_fmt(d.upper_bound);
                            }
                        }
                        return prefix + value_str +
                            " " + plot.cfg.y.tip_lbl + " by " +
                            date_str(d.date);
                    });
            }
            // Plot the peak timing predictions.
            if (plot.cfg.plot_type == "peak") {
                //
                // Plot the predicted peak timing data.
                //

                plot.contents.title.text("Predicted peak timing");

                for (cint of plot.df.cints.reverse()) {
                    if (plot.series[cint] === undefined) {
                        plot.series[cint] = {};
                        plot.series[cint].area = plot.contents.append(p);
                        plot.series[cint].lmin = plot.contents.append(p);
                        plot.series[cint].lmax = plot.contents.append(p);
                        plot.series[cint].area
                            .style("opacity", 1);
                    }

                    c_data = plot.df[cint];

                    // Draw the credible interval region.
                    plot.series[cint].area.data([c_data])
                        .attr("class", "area " + c_class[cint])
                        .attr("d", plot.draw.area);
                    // Draw the credible interval lower bound.
                    plot.series[cint].lmin.data([c_data])
                        .attr("class", "series " + c_class[cint])
                        .attr("d", plot.draw.minline);
                    // Draw the credible interval upper bound.
                    plot.series[cint].lmax.data([c_data])
                        .attr("class", "series " + c_class[cint])
                        .attr("d", plot.draw.maxline);
                }

                plot.contents.selectAll(".truth")
                    .data([0])
                    .enter()
                    .append("svg:line")
                    .attr("class", "truth")
                    // Add a mouse-over title to identify this data series.
                    .append("svg:title")
                    .attr("class", "truth_title");
                plot.contents.selectAll(".truth")
                    .attr("x1", plot.axis.x(plot.df.lims.x0))
                    .attr("x2", plot.axis.x(plot.df.lims.x1))
                    .attr("y1", plot.axis.y(plot.df.truth))
                    .attr("y2", plot.axis.y(plot.df.truth));
                plot.contents.selectAll(".truth_title")
                    .text("Observed peak: " + date_str(plot.df.truth));

                // Draw a vertical line indicating the current forecasting date.
                if (plot.fs_date !== undefined) {
                    fs_as_date = new Date(plot.fs_date);
                    plot.contents.selectAll(".at_fs_date")
                        .data([0])
                        .enter()
                        .append("svg:line")
                        .attr("class", "at_fs_date")
                        .append("svg:title")
                        .attr("class", "at_fs_date_title");
                    plot.contents.selectAll(".at_fs_date")
                        .attr("x1", plot.axis.x(fs_as_date))
                        .attr("x2", plot.axis.x(fs_as_date))
                        .attr("y1", plot.axis.y(plot.df.lims.y0))
                        .attr("y2", plot.axis.y(plot.df.lims.y1));
                    plot.contents.selectAll(".at_fs_date_title")
                        .text("Forecasting date: " + date_str(fs_as_date));
                }
            }

        };

        plot.update();
        if (plot.cfg.plot_type == "fs") {
            Plot.connect_slider(plot);
        }
    };
};

/**
 *
 */
Plot.begin_loading = function(plot, selected_file) {
    "use strict";
    var data_file = plot.cfg.default_file;
    if (selected_file !== undefined) {
        data_file = selected_file;
    }
    // Asynchronously load the plot data.
    d3.json(data_file, Plot.loader(plot));
};

/**
 * Create an SVG plot.
 */
Plot.create = function(config, span_id) {
    "use strict";
    if (Plot.created_plots === undefined) {
        // Create an array to store each plot.
        Plot.created_plots = [];
    }

    // Construct a group element (inside an SVG element) and obtain a
    // namespace in which to record the plot elements and associated data.
    var plot = Plot.make_svg(config, span_id);
    Plot.begin_loading(plot);
    Plot.created_plots.push(plot);
    return plot;
};

// Start at the most recent forecasts unless 'start' is in the query string.
Plot.most_recent_first = true;
var url_params = location.search.substring(1).split("&");
for (var p of url_params) {
    if (p == "start") {
        Plot.most_recent_first = false;
        break;
    }
}
// Now that the season is over, start at the earliest forecast.
Plot.most_recent_first = false;

Plot.default_width = document.getElementById("content").offsetWidth * 0.6;
if (Plot.default_width <= 480) {
    Plot.default_width = document.getElementById("content").offsetWidth;
}
Plot.default_height = Math.min(0.75 * Plot.default_width,
                               0.90 * document.documentElement.clientHeight);

Plot.default_config = function(default_file) {
    "use strict";
    if (typeof default_file === "undefined") {
        default_file = "";
    }
    return({
        dims: {
            w: Plot.default_width, h: Plot.default_height,
            padding_x: 75, padding_y: 50,
            margin_pcnt: 0.01
        },
        draw_box: false,
        most_recent_first: Plot.most_recent_first,
        stop_at_end: true,
        default_file: default_file,
        default_speed: 2000,
        plot_type: "fs",
        x: Plot.date_axis("Date"),
        y: Plot.num_axis("Weekly Influenza Notifications", 0)});
};

Plot.peak_config = function(default_file) {
    "use strict";
    if (typeof default_file === "undefined") {
        default_file = "";
    }
    var y = Plot.date_axis("Predicted Peak");
    y.fmt_tick = d3.time.format("%b %-d");
    y.tick = 8;
    return({
        dims: {
            w: Plot.default_width, h: Plot.default_height,
            padding_x: 75, padding_y: 50,
            margin_pcnt: 0.01
        },
        draw_box: false,
        most_recent_first: Plot.most_recent_first,
        stop_at_end: true,
        default_file: default_file,
        default_speed: 2000,
        plot_type: "peak",
        x: Plot.date_axis("Forecasting Date"),
        y: y});
};

// Adjust plot sizes when the window size changes.
d3.select(window).on("resize", Plot.resize);
