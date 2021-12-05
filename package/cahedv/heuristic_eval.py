# Importing Required libraries
import plotly.express as px
import json
from enum import Enum, auto
from colorama import Fore
import math
from colour import Color

# Important functions
def to_json_string(str):
    json_obj = json.loads(str)
    json_formatted_str = json.dumps(json_obj, indent = 2)
    return json_formatted_str

def to_json(str):
  return json.loads(str)

def print_json(plot):
  json_obj = to_json_string(plot.to_json())
  print(json_obj)


def get_layout(json):
  if IMP_STRS.LAYOUT in json:
    return json[IMP_STRS.LAYOUT]
  return None

def get_data(json):
  if IMP_STRS.DATA in json:
    return json[IMP_STRS.DATA]
  return None

def check_title_in_json(layout):
  if IMP_STRS.TITLE in layout:
    title = layout[IMP_STRS.TITLE]

    if IMP_STRS.TEXT in title and title[IMP_STRS.TEXT].strip() != "":
      return True

  return False

def getColorValue(hexValue):
    return Color(hexValue).luminance


def isLightColor(hexValue):
    # print(hexValue, hsp)
    return getColorValue(hexValue) > 0.5

def check_equal_list(lst):
    res = False
    if len(lst) < 0 :
        res = True
    res = all(ele == lst[0] for ele in lst)
    return res

def check_nticks(value):
  return value >= 4 and value <= 12

def get_float_values(arr):
  farr = []
  for val in arr:
    try:
      farr.append(float(val))
    except ValueError:
      pass
  return farr
    
class Attributes(Enum):
  VISUAL_FRAMES_SINGLE = auto()
  VISUAL_FRAMES_MULTIPLE = auto()
  
  VISUAL_STRUCTURES_SCATTER_PLOT = auto()
  VISUAL_STRUCTURES_LINE_PLOT = auto()
  VISUAL_STRUCTURES_BAR_PLOT = auto()
  VISUAL_STRUCTURES_PIE_CHART = auto()
  VISUAL_STRUCTURES_3D = auto()

  VISUAL_UNITIES_POINTS = auto()
  VISUAL_UNITIES_LINES = auto()
  VISUAL_UNITIES_2D_SHAPES = auto()
  VISUAL_UNITIES_TEXTS = auto()
  VISUAL_UNITIES_TOOLTIPS = auto()

  VISUAL_PRIMITIVES_X_POS = auto()
  VISUAL_PRIMITIVES_Y_POS = auto()
  VISUAL_PRIMITIVES_SHAPE = auto()
  VISUAL_PRIMITIVES_SIZE = auto()
  VISUAL_PRIMITIVES_COLOR = auto()

  LABELING_CHART_TITLE = auto()
  LABELING_AXIS = auto()
  LABELING_LEGEND = auto()

  INTERACTION_TOOLTIP = auto()
  INTERACTION_ZOOM = auto()
  INTERACTION_PAN = auto()
  INTERACTION_FILTER = auto()

  DATA_RANGE = auto()
  DATA_DIMENSION = auto()
  DATA_NUMERICAL = auto()
  DATA_CONTINUOUS = auto()

class RULETYPES(Enum):
  DIFFICULT_TO_CHECK = auto()
  ADVICE = auto()
  AUTOMATIC_CHECK = auto()

class IMP_STRS:
  TITLE = "title"
  LAYOUT = "layout"
  TEXT = "text"
  X_AXIS = "xaxis"
  Y_AXIS = "yaxis"
  DATA = "data"
  PIE = "pie"
  BAR = "bar"
  TYPE = "type"
  SCATTER = "scatter"
  LINES = "lines"
  THREE_D = "3d"
  MODE = "mode"
  COLOR = "color"
  COLOR_AXIS = "coloraxis"
  MARKER = "marker"
  MARKERS = "markers"
  GRID_COLOR = "gridcolor"
  ZERO_LINE_COLOR = "zerolinecolor"
  LABELS = "labels"
  VALUES = "values"
  COLORS = "colors"
  SIZE = "size"
  X = "x"
  Y = "y"
  Z = "z"
  NTICKS = "nticks"
  DTICK = "dtick"
  FIXED_RANGE = "fixedrange"
  DISPLAY_MODE = "displayModeBar"
  HOVER_TEMPLATE = "hovertemplate"
  BAR_MODE = "barmode"
  GROUP = "group"
  STACK = "stack"
  NAME = "name"

class RULE(object):

  def __init__(self, desp, attr, type):
    self.description = desp
    self.attributes = attr
    self.type = type
  
  def evaluate(self, plot_json):
    strs = []
    if self.type == RULETYPES.DIFFICULT_TO_CHECK:
      str.append('Internal Error: These rules should not be used by program') 
    elif self.type == RULETYPES.ADVICE:
      pass
    elif self.type == RULETYPES.AUTOMATIC_CHECK:
      strs.append('Internal Error: This function should be implemented')
    else:
      strs.append('Internal Error: This should not be reachable')
    return False, strs

class RULE1(RULE):

  def __init__(self):

    super().__init__("A plot should have a title",
                   [Attributes.LABELING_CHART_TITLE],
                   RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, plot_json):
    if IMP_STRS.LAYOUT in plot_json:
      layout = plot_json[IMP_STRS.LAYOUT]

      check = check_title_in_json(layout)
      if check:
        return True, []

    return False, ["Title is missing for the plot"]

class RULE2(RULE):

  def __init__(self):

    super().__init__("Each Axis should have a label",
                     [Attributes.LABELING_AXIS],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, plot_json):
    has_x_title, has_y_title = False, False
    if IMP_STRS.LAYOUT in plot_json:
      layout = plot_json[IMP_STRS.LAYOUT]
      
      if IMP_STRS.X_AXIS in layout:
        x_axis = layout[IMP_STRS.X_AXIS]
        has_x_title = check_title_in_json(x_axis)

      if IMP_STRS.Y_AXIS in layout:
        y_axis = layout[IMP_STRS.Y_AXIS]
        has_y_title = check_title_in_json(y_axis)
    
    ans = []
    if not has_x_title:
      ans.append("X-axis is not labeled")
    if not has_y_title:
      ans.append("Y-axis is not labeled")
    
    if len(ans) == 0:
      return True, []
    else:
      return False, ans 

class RULE3(RULE):

  def __init__(self):

    super().__init__("Consider replacing a pie chart with a bar chart",
                   [Attributes.VISUAL_STRUCTURES_PIE_CHART],
                   RULETYPES.ADVICE)

class RULE4(RULE):

  def __init__(self):

    super().__init__("Avoid using more than four different colors",
                   [Attributes.VISUAL_PRIMITIVES_COLOR],
                   RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, plot_json):
    data = get_data(plot_json)
    if data is None:
      return
    
    colors_used = {}
    color_axis = 0
    for item in data:
      if IMP_STRS.MARKER in item:
        marker = item[IMP_STRS.MARKER]
        if IMP_STRS.COLOR_AXIS in marker:
          color_axis = 1
        if IMP_STRS.COLOR in marker:
          colors_used[IMP_STRS.COLOR] = 1
    
    if len(colors_used) > 4:
      return False, ["Used More than four colors"]
    
    if color_axis == 1:
      return False, ["Used Color axis which is similar to using more than 4 colors"]
    
    return True, []

class RULE5(RULE):

  def __init__(self):
    super().__init__("Use a lighter color for secondary elements such as frames, grids, and axes",
                     [Attributes.VISUAL_PRIMITIVES_COLOR],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    data = get_layout(json)
    if data is None:
      return True, []
    
    ans = []
    if IMP_STRS.X_AXIS in data:
      xaxis = data[IMP_STRS.X_AXIS]
      if IMP_STRS.GRID_COLOR in xaxis:
        if not isLightColor(xaxis[IMP_STRS.GRID_COLOR]):
          ans.append("Grid color should not be dark")

      if IMP_STRS.ZERO_LINE_COLOR in xaxis:
        if not isLightColor(xaxis[IMP_STRS.ZERO_LINE_COLOR]):
          ans.append("X-Axis color should not be dark")


    if IMP_STRS.Y_AXIS in data:
      xaxis = data[IMP_STRS.Y_AXIS]
      if IMP_STRS.GRID_COLOR in xaxis:
        if not isLightColor(xaxis[IMP_STRS.GRID_COLOR]):
          ans.append("Grid color should not be dark")

      if IMP_STRS.ZERO_LINE_COLOR in xaxis:
        if not isLightColor(xaxis[IMP_STRS.ZERO_LINE_COLOR]):
          ans.append("Y-Axis color should not be dark")
    
    if len(ans) == 0:
      return True, []
    else:
      return False, ans

class RULE6(RULE):

  def __init__(self):
    super().__init__("Preserve data to graphic dimensionality. For example, avoid representing one or two-dimensional data in 3D visualizations.",
                     [Attributes.VISUAL_STRUCTURES_3D, Attributes.DATA_DIMENSION],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, plot_json):
    data = get_data(plot_json)
    if data is None:
      return True, []
    
    ans = 0
    for item in data:
      vals = [IMP_STRS.X, IMP_STRS.Y, IMP_STRS.Z]
      for val in vals:
        if val in item:
          if check_equal_list(item[val]):
            ans = 1
    
    if ans:
      return False, ["Don't represent 1D or 2D data in 3D visualizations"]
    else:
      return True, []

class RULE7(RULE):

  def __init__(self):
    super().__init__("Color perception varies with the size of the colored item.",
                     [Attributes.VISUAL_PRIMITIVES_SIZE, Attributes.VISUAL_PRIMITIVES_COLOR],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def compare_color_size(self, size_color):
    rule_fail = False
    n = len(size_color)
    for i in range(0, n):
      val1 = size_color[i]
      for j in range(i + 1, n):
        val2 = size_color[j]
        if (val1[0] > val2[0]) and (val1[1] >= val2[1]):
          rule_fail = True

    return rule_fail
  
  def evaluate(self, plot_json):
    data = get_data(plot_json)
    size_color = []
    for item in data:
      if IMP_STRS.MARKER in data:
        marker = data[IMP_STRS.MARKER]
        if (IMP_STRS.COLOR in marker) and (IMP_STRS.SIZE in marker):
          size_color.append((float(marker[IMP_STRS.SIZE]), getColorValue(marker[IMP_STRS.COLOR])))
    n = len(size_color)

    rule_fail = self.compare_color_size(size_color)
    
    datas = data
    for data in datas:
      if IMP_STRS.TYPE in data:
        if data[IMP_STRS.TYPE] == IMP_STRS.PIE:
          labels = data[IMP_STRS.LABELS] if IMP_STRS.LABELS in data else []
          
          values = data[IMP_STRS.VALUES] if IMP_STRS.VALUES in data else []
          values = get_float_values(values)

          colors = data[IMP_STRS.MARKER][IMP_STRS.COLORS] if (IMP_STRS.MARKER in data) and (IMP_STRS.COLORS in data[IMP_STRS.MARKER])  else []
          colors = [getColorValue(color) for color in colors]


          size_color = {}
          if len(labels) == len(values) and len(values) == len(colors):
            for i in range(0,len(labels)):
              if labels[i] not in size_color:
                size_color[labels[i]] = (values[i], colors[i])
              else:
                value = size_color[labels[i]][0]
                size_color[labels[i]] = (value + values[i], size_color[labels[i]][1])

            # print(size_color)

            size_color_f = [v for _, v in size_color.items()]
            rule_fail = self.compare_color_size(size_color_f)
    
    if rule_fail:
      return False, ["Larger Sizes should have dark color"] 
    else:
      return True, []

class RULE8(RULE):

  def __init__(self):
    super().__init__("Do not use line plots if wild points are at all common",
                     [Attributes.VISUAL_STRUCTURES_LINE_PLOT],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    check_3d = check_if_3D_visualization(json)
    ans = True
    if check_3d:
      pass
    else:
      data = get_data(json)

      if data is not None:
        for item in data:
          x = item[IMP_STRS.X] if (IMP_STRS.X in item) else []
          y = item[IMP_STRS.Y] if (IMP_STRS.Y in item) else []
          if len(x) == len(y) and len(x) > 1:
            prev_slope = None
            for i in range(0, len(x) - 1):
              x1, y1, x2, y2 = x[i], y[i], x[i + 1], y[i + 1]
              curr_slope = None
              if x1 == x2:
                curr_slope = math.inf
              else:
                curr_slope = (y2 - y1) / (x2 - x1)
              
              if prev_slope != None:
                if abs(prev_slope) * 0.4 < abs(curr_slope - prev_slope): 
                  ans = False
              prev_slope = curr_slope
      
    if ans == False:
      return False, ["Too much difference in slopes of the lines. Line Plot might not be the appropriate plot in this case"]
    else:
      return True, []

class RULE9(RULE):

  def __init__(self):
    super().__init__("For a scatter plot [where dependence of y upon value of x is the focus of the plot), it is unlikely that linking up into a chain is sensible and useful" + "\n" 
                     + "What we are likely to want from a scatter plot are indications of tilting, or arching up or sagging down, or of horizontal wedging" + "\n" 
                     + "- Use a scatter plot only when it is useful",
                     [Attributes.VISUAL_STRUCTURES_SCATTER_PLOT],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    data = get_data(json)
    if data is not None:
      return True, []
    
    ans = []
    for item in data:
      x = item[IMP_STRS.X] if (IMP_STRS.X in item) else []
      y = item[IMP_STRS.Y] if (IMP_STRS.Y in item) else []
      if check_equal_list(x):
        ans.append("All the X co-ordinates are the same. Try using another plot")
      if check_equal_list(y):
        ans.append("All the Y co-ordinates are the same. Try using another plot")

    return (len(ans) == 0), ans

class RULE10(RULE):

  def __init__(self):
    super().__init__("A reasonable number of reference values on a coordinate axis might be between four and twelve",
                     [Attributes.LABELING_AXIS],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    data = get_data(json)
    layout = get_layout(json)
    if data is None or layout is None:
      return True, []
    
    xaxis = layout[IMP_STRS.X_AXIS] if IMP_STRS.X_AXIS in layout else None
    yaxis = layout[IMP_STRS.Y_AXIS] if IMP_STRS.Y_AXIS in layout else None

    ans = []

    if xaxis is not None:
      if IMP_STRS.NTICKS in xaxis:
        if not check_nticks(float(xaxis[IMP_STRS.NTICKS])): 
          ans.append("X-axis has too many reference values. Ideal values are between 4 and 12")
      
      if IMP_STRS.DTICK in xaxis:
        dtick = xaxis[IMP_STRS.DTICK]
        for item in data:
          if IMP_STRS.X in item:
            xvals = get_float_values(item[IMP_STRS.X])
            maxi, mini = max(xvals), min(xvals)
        
        if not check_nticks((maxi - mini) / dtick): 
          ans.append("X-axis has too many reference values. Ideal values are between 4 and 12")

    if yaxis is not None:
      if IMP_STRS.NTICKS in yaxis:
        if not check_nticks(yaxis[IMP_STRS.NTICKS]): 
          ans.append("Y-axis has too many reference values. Ideal values are between 4 and 12")

      if IMP_STRS.DTICK in yaxis:
        dtick = yaxis[IMP_STRS.DTICK]
        for item in data:
          if IMP_STRS.Y in item:
            yvals = get_float_values(item[IMP_STRS.Y])
            maxi, mini = max(yvals), min(yvals)
        
        if not check_nticks((maxi - mini) / dtick): 
          ans.append("Y-axis has too many reference values. Ideal values are between 4 and 12")

    return len(ans) == 0, ans

class RULE11(RULE):

  def __init__(self):
    super().__init__("Zoom, Filter and Details on Demand",
                     [[Attributes.INTERACTION_ZOOM, Attributes.INTERACTION_FILTER, Attributes.INTERACTION_TOOLTIP, Attributes.INTERACTION_PAN]],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    ans = []
    if check_tooltip(json):
      ans.append("Show tooltips when hovered")

    layout = get_layout(json)
    if layout is not None:
      if IMP_STRS.X_AXIS in layout:
        if IMP_STRS.FIXED_RANGE in layout[IMP_STRS.X_AXIS] and layout[IMP_STRS.X_AXIS][IMP_STRS.FIXED_RANGE] == True:
          ans.append("Zoom, Pan on demand of user")

      if IMP_STRS.Y_AXIS in layout:
        if IMP_STRS.FIXED_RANGE in layout[IMP_STRS.Y_AXIS] and layout[IMP_STRS.Y_AXIS][IMP_STRS.FIXED_RANGE] == True:
          ans.append("Zoom, Pan on demand of user")
    
    return len(ans) == 0, ans

class RULE12(RULE):

  def __init__(self):
    super().__init__("Multivariate data calls for multivariate representation" + "\n"
                    + "One implication is to consider replacing a stacked bar chart with multiple bar charts or re-chart placing a grouped bar chart with a scatter plot with color-coding.",
                     [Attributes.VISUAL_STRUCTURES_BAR_PLOT],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    data = get_data(json)
    
    arr = []
    ans = True
    for item in data:
      if IMP_STRS.TYPE in item and item[IMP_STRS.TYPE] == IMP_STRS.BAR:
        temp = [item[IMP_STRS.X_AXIS], item[IMP_STRS.Y_AXIS]]
        if temp in arr:
          ans = False
        else:
          arr.append(temp)
    
    layout = get_layout(json)
    final_strs = []
    if not ans:
      if layout is None:
        final_strs.append("R: Consider replacing a stacked bar chart with multiple bar charts")
      else:
        if IMP_STRS.BAR_MODE in layout:
          if layout[IMP_STRS.BAR_MODE] == IMP_STRS.GROUP:
            final_strs.append("R: Re-chart placing a grouped bar chart with a scatter plot with color-coding")
          else:
            final_strs.append("R: Consider replacing a stacked bar chart with multiple bar charts")
        else:
          final_strs.append("R: Consider replacing a stacked bar chart with multiple bar charts")


    return len(final_strs) == 0, final_strs

class RULE13(RULE):

  def __init__(self):
    super().__init__("Differential sensitivity for area is 6.0 percent. This value implies that for differences in area to be detectable, the areas must differ by 6.0 percent or more. \n" +
                     "The difference between two sections of a plot should be greater than 6 percent.", 
                     [Attributes.VISUAL_STRUCTURES_PIE_CHART],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def get_value(self, value):
    if type(value) == str:
      return 1
    else:
      return value
  
  def evaluate(self, json):
    ans = True
    datas = get_data(json)
    strs = []
    if datas is None:
      return True, strs

    for data in datas:
      if IMP_STRS.TYPE in data:
        if data[IMP_STRS.TYPE] == IMP_STRS.PIE:
          labels = data[IMP_STRS.LABELS] if IMP_STRS.LABELS in data else []
          
          values = data[IMP_STRS.VALUES] if IMP_STRS.VALUES in data else []
          values = get_float_values(values)

          percent = {}
          total = 0
          if len(labels) == len(values):
            for i in range(0, len(labels)):
              total += self.get_value(values[i])
              if labels[i] not in percent:
                percent[labels[i]] = self.get_value(values[i])
              else:
                percent[labels[i]] += self.get_value(values[i])
          
          if total > 0:
            list_per = list(percent.values())
            list_per.sort()
            percent_values = [(val / total) * 100 for val in list_per]
            for i in range(0, len(percent_values) - 1):
              if (percent_values[i + 1] - percent_values[i]) < 0.06 * percent_values[i]:
                ans = False
                strs.append("W:" + str(percent_values[i + 1]) + " " + str(percent_values[i]) + " are causing problem")

                    
    if ans:
      return True, []
    else:
      return False, ["The difference between areas of two consecutive sections of a plot should be greater than 6 percent to be detectable."] + strs

class RULE14(RULE):

  def __init__(self):
    super().__init__("Ensure the visual variable has sufficient length",
                     [[Attributes.VISUAL_STRUCTURES_BAR_PLOT]],
                     RULETYPES.AUTOMATIC_CHECK)
  
  def evaluate(self, json):
    ans = True
    datas = get_data(json)
    
    if datas is None:
      return True, []

    types = set()
    strs = set()
    for data in datas:
      if IMP_STRS.TYPE in data:
        if data[IMP_STRS.TYPE] == IMP_STRS.BAR:
          x = data[IMP_STRS.X]
          set_x = set(x)
          map_x = {}

          for val in set_x:
            req = (str(val),"")
            if IMP_STRS.NAME in data:
              req = (str(val), str(data[IMP_STRS.NAME])) 
            if req not in types:
              types.add(req)
            map_x[req] = x.count(val)

          for val in types:
            if val not in map_x:
              if IMP_STRS.NAME in data:
                if val[1] == data[IMP_STRS.NAME]:
                  strs.add(val)
              else:
                strs.add(val)
    
    if len(strs) == 0:
      return True, []
    else:
      problems = ["" + val[0] + " " + val[1] + " - this variable is causing problems" for val in strs]
      return False, ["There should be atleast one value of the visible variable"] + problems


    pass

class RULE15(RULE):

  def __init__(self):
    super().__init__("Even a basically good set of symbols will become indistinct if either \n" + 
                     "(i) they are plotted too small, \n" + 
                     "(ii) the points are too numerous or overlap excessively, or \n" + 
                     "(iii) too many categories are represented.",
                     [Attributes.VISUAL_STRUCTURES_SCATTER_PLOT],
                     RULETYPES.ADVICE)

class RULE_(RULE):

  def __init__(self):
    super().__init__()
  
  def evaluate(self, json):
    pass


def has_axis(json):
  # if (json_check(json, [IMP_STRS.LAYOUT, IMP_STRS.X_AXIS])) or (json_check(json, [IMP_STRS.LAYOUT, IMP_STRS.Y_AXIS])):
  #   return True
  layout = get_layout(json)
  if layout is not None:
    if IMP_STRS.X_AXIS in layout or IMP_STRS.Y_AXIS in layout:
      return True
  return False

def extract_labeling(json):
  attrs = []
  attrs.append(Attributes.LABELING_CHART_TITLE)
  if has_axis(json):
    attrs.append(Attributes.LABELING_AXIS)

  return attrs

def check_has_pie_chart(json):
  data = get_data(json)
  if data is not None:
    for item in data:
      if IMP_STRS.TYPE in item:
        if item[IMP_STRS.TYPE] == IMP_STRS.PIE:
          return True
  return False

def check_has_bar_chart(json):
  data = get_data(json)
  if data is not None:
    for item in data:
      if IMP_STRS.TYPE in item:
        if item[IMP_STRS.TYPE] == IMP_STRS.BAR:
          return True
  return False

def check_has_line_plot(json):
  data = get_data(json)
  if data is not None:
    for item in data:
      if IMP_STRS.TYPE in item:
        if IMP_STRS.SCATTER in item[IMP_STRS.TYPE]:
          if IMP_STRS.MODE in item:
            if IMP_STRS.LINES in item[IMP_STRS.MODE]:
              return True 
  
  return False

def check_has_scatter_plot(json):
  data = get_data(json)
  if data is not None:
    for item in data:
      if IMP_STRS.TYPE in item:
        if IMP_STRS.SCATTER in item[IMP_STRS.TYPE]:
          if IMP_STRS.MODE in item:
            print(item[IMP_STRS.MODE])
            if IMP_STRS.MARKERS == item[IMP_STRS.MODE]:
              return True 

def check_if_3D_visualization(json):
  data = get_data(json)
  if data is not None:
    for item in data:
      if IMP_STRS.TYPE in item:
        if IMP_STRS.THREE_D in item[IMP_STRS.TYPE]:
          return True
  return False

def extract_visual_structures(json):
  attrs = []
  if check_has_pie_chart(json):
    attrs.append(Attributes.VISUAL_STRUCTURES_PIE_CHART)
  if check_has_line_plot(json):
    attrs.append(Attributes.VISUAL_STRUCTURES_LINE_PLOT)
  if check_if_3D_visualization(json):
    attrs.append(Attributes.VISUAL_STRUCTURES_3D)
  if check_has_bar_chart(json):
    attrs.append(Attributes.VISUAL_STRUCTURES_BAR_PLOT)
  if check_has_scatter_plot(json):
    attrs.append(Attributes.VISUAL_STRUCTURES_SCATTER_PLOT)

  return attrs

def marker_has_color(json):
  data = get_data(json)
  if data is None:
    return False
  
  for item in data:
    if IMP_STRS.MARKER in item:
      marker = item[IMP_STRS.MARKER]
      if (IMP_STRS.COLOR in marker) or (IMP_STRS.COLORS in marker):
        return True
  return False

def has_label_pie(json):
  data = get_data(json)
  if data is None:
    return False
  pie_chart = check_has_pie_chart(json)
  if pie_chart:
    for item in data:
      if IMP_STRS.LABELS in item:
        return True
  return False

def marker_has_size(json):
  data = get_data(json)
  if data is None:
    return False
  
  for item in data:
    if IMP_STRS.MARKER in item:
      marker = item[IMP_STRS.MARKER]
      if IMP_STRS.SIZE in marker:
        return True

def color_involved_in_secondary_elements(json):
  data = get_layout(json)
  if data is None:
    return False
  
  if IMP_STRS.X_AXIS in data:
    xaxis = data[IMP_STRS.X_AXIS]
    if (IMP_STRS.GRID_COLOR in xaxis) or (IMP_STRS.ZERO_LINE_COLOR in xaxis):
      return True
  
  if IMP_STRS.Y_AXIS in data:
    yaxis = data[IMP_STRS.Y_AXIS]
    if (IMP_STRS.GRID_COLOR in yaxis) or (IMP_STRS.ZERO_LINE_COLOR in yaxis):
      return True
  
  return False
    
def extract_visual_primitives(json):
  attrs = []

  if marker_has_color(json) or color_involved_in_secondary_elements(json):
    attrs.append(Attributes.VISUAL_PRIMITIVES_COLOR)
  
  if marker_has_size(json) or has_label_pie(json):
    attrs.append(Attributes.VISUAL_PRIMITIVES_SIZE)

  return attrs

def extract_visual_frames(json):
  arr = []
  return arr

def check_tooltip(json):
  data = get_data(json)
  if data is None:
    return False
  
  for item in data:
    if IMP_STRS.HOVER_TEMPLATE not in item:
      return True
    elif item[IMP_STRS.HOVER_TEMPLATE] == "":
      return True
  
  return False

def check_pan_zoom(json):
  layout = get_layout(json)
  if layout is None:
    return False
  
  if IMP_STRS.X_AXIS in layout:
    if IMP_STRS.FIXED_RANGE in layout[IMP_STRS.X_AXIS]:
      return True

  if IMP_STRS.Y_AXIS in layout:
    if IMP_STRS.FIXED_RANGE in layout[IMP_STRS.Y_AXIS]:
      return True
  
  return False

def extract_interaction(json):
  arr = []
  if check_tooltip(json):
    arr.append(Attributes.INTERACTION_TOOLTIP)
  if check_pan_zoom(json):
    arr.append(Attributes.INTERACTION_ZOOM)
    arr.append(Attributes.INTERACTION_PAN)
  return arr

def match_attrs(attrs, rule_attrs):
  for rule_attr in rule_attrs:
    if isinstance(rule_attr, list):
      # Checking if plot has anyone of the optional attributes of the rule
      found = False
      for optional_attr in rule_attr:
        if optional_attr in attrs:
          found = True
      
      if found == False:
        return False
    
    elif rule_attr not in attrs:
      return False  
  return True

def extract_attributes_of_plot(json_obj):

  # TODO - extracting attributes from json one by one
  attrs = []
  attrs = attrs + extract_visual_frames(json_obj)
  attrs = attrs + extract_visual_structures(json_obj)
  attrs = attrs + extract_labeling(json_obj)
  attrs = attrs + extract_visual_primitives(json_obj)
  attrs = attrs + extract_interaction(json_obj)
  return attrs

def extract_rules_matching_plot(attrs):
  # TODO - matching the attributes extracted of the plots and finding the rules which match them
  rules = [RULE1(), RULE2(), RULE3(), RULE4(), RULE5(), RULE6(), RULE7(), RULE8(), RULE9(), RULE10(), RULE11(), RULE12(), RULE13(), RULE14(), RULE15()]
  matched = []

  for rule in rules:
    if match_attrs(attrs, rule.attributes):
      matched.append(rule)

  return matched

def evaluation(rules, json_plot):
  final_outputs = []
  for rule in rules:
    followed, evals = rule.evaluate(json_plot)
    curr_item = {}
    curr_item["rule"] = rule.description
    curr_item["type"] = rule.type.value
    curr_item["status"] = followed
    curr_item["warnings"] = evals   
    final_outputs.append(curr_item)   
  return final_outputs

def evaluation_print(rules, json_plot):
  final_outputs = []
  for rule in rules:
    followed, evals = rule.evaluate(json_plot)
    if rule.type == RULETYPES.ADVICE:
      # Advices are just given so that user can check what them manually
      print(Fore.BLUE + "Advice: " + rule.description)

    elif rule.type == RULETYPES.AUTOMATIC_CHECK:
      # Consider this to be the main part
      color = Fore.GREEN if followed else Fore.RED
      print(color + "Evaluted: " + rule.description)
      if not followed:
        for eval in evals:
          print(Fore.YELLOW + eval)
    
    print()
  
  return final_outputs

# This is the API called by the user
def heuristic_eval(plot_str):

  # convert the object to json
  plot_json = to_json(plot_str)

  # Identify the attributes present in the plot
  attrs = extract_attributes_of_plot(plot_json)
  print(attrs)

  # Extract the rules that are matching the plot
  rules = extract_rules_matching_plot(attrs)

  # Evaluate the rules which can be evaluated - give warning if something is wrong
  # For rules which are of type advice - give recommendations
  # returned as a array
  return evaluation(rules, plot_json)