from .teleport import *
from .material import *
from .rappture import *
from .plotly import *

import ipywidgets as widgets
from traitlets import Unicode, Integer, validate, Bool, Float, TraitError, Dict, List, Any, Instance
import xml, re, json, uuid
from IPython.display import HTML, Javascript, display

def buildWidget(Project, *args, **kwargs):
    component = Project.project_name      
    Project.root.name_component = component
    eol = "\n";
    
    attrs = {
    }
    
    default = {
    }
    
    functions = {
    }
    
    for i,d in Project.root.propDefinitions.items():  
        if d['type'] == "func":
            attrs[i] = lambda s, c, r=False, m=i : getattr(s,'_handlers_'+ m).register_callback(c, r)            
            functions[i] =  (d['defaultValue'])
            Project.root.propDefinitions[i]['type'] = "func"
            Project.root.propDefinitions[i]['defaultValue']="(e)=>{ if (event) event.preventDefault(); backbone.send({ event: '" + i + "', 'params' : (" + d['defaultValue'] + ")(e) });}"
    parseState = ""
    serializers = []
    for i,d in Project.root.stateDefinitions.items():  
        parseState += "        if('"+i+"' in state){" + eol
        if d['type'] == "string":
            parseState += "          state['"+i+"'] = String(state['"+i+"']);" + eol
            default[i] =  str(d['defaultValue'])
            attrs[i] = Unicode(default[i]).tag(sync=True)
            Project.root.stateDefinitions[i]['type'] = "func"
            Project.root.stateDefinitions[i]['defaultValue']="backbone.model.get('"+i+"')"
        elif d['type'] == "boolean":
            parseState += "          state['"+i+"'] = [true, 'true', 'True', 'on', 'yes', 'Yes', 'TRUE', 1, 'ON'].includes(state['"+i+"']);" + eol
            default[i] = (d['defaultValue'] in [True, "true", "True", "on", "yes", "Yes", "TRUE", 1, "ON"])
            attrs[i] = Bool(default[i]).tag(sync=True)
            Project.root.stateDefinitions[i]['type'] = "func"
            Project.root.stateDefinitions[i]['defaultValue']="backbone.model.get('"+i+"')"

        elif d['type'] == "number":
            parseState += "          state['"+i+"'] = parseFloat(state['"+i+"']);" + eol
            default[i] = float(d['defaultValue'])
            attrs[i] = Float(default[i]).tag(sync=True)
            Project.root.stateDefinitions[i]['type'] = "func"
            Project.root.stateDefinitions[i]['defaultValue']="backbone.model.get('"+i+"')"

        elif d['type'] == "integer":
            parseState += "          state['"+i+"'] = parseInt(state['"+i+"']);" + eol
            default[i] = int(d['defaultValue'])
            attrs[i] = Integer(default[i]).tag(sync=True)
            Project.root.stateDefinitions[i]['type'] = "func"
            Project.root.stateDefinitions[i]['defaultValue']="backbone.model.get('"+i+"')"

        elif d['type'] == "object":
            parseState += "          state['"+i+"'] = (state['"+i+"']);" + eol
            default[i] = dict(d['defaultValue'])
            attrs[i] = Dict(default[i]).tag(sync=True)
            Project.root.stateDefinitions[i]['type'] = "func"
            Project.root.stateDefinitions[i]['defaultValue']="backbone.model.get('"+i+"')"

        elif d['type'] == "array":
            parseState += "          state['"+i+"'] = (state['"+i+"']);" + eol
            default[i] = list(d['defaultValue'])
            attrs[i] = List(default[i]).tag(sync=True)
            Project.root.stateDefinitions[i]['type'] = "func"
            Project.root.stateDefinitions[i]['defaultValue']="backbone.model.get('"+i+"')"

        elif d['type'] == "router": #missuse of router to mark widgets arrays
            parseState += "          state['"+i+"'] = (state['"+i+"']);" + eol
            default[i] = list()
            attrs[i] = widgets.trait_types.TypedTuple(trait=Instance(widgets.Widget)).tag(sync=True, **widgets.widget_serialization)
            Project.root.stateDefinitions[i]['type'] = "array"
            Project.root.stateDefinitions[i]['defaultValue']=[]
            serializers.append(i)
        parseState += "        }" + eol


    
    js = ""
    js += "require.config({" + eol
    js += "  paths: {" + eol
    js += "    'react': 'https://unpkg.com/react@16.8.6/umd/react.development'," + eol
    js += "    'react-dom': 'https://unpkg.com/react-dom@16.8.6/umd/react-dom.development'," + eol
    js += "    'material-ui': 'https://unpkg.com/@material-ui/core@latest/umd/material-ui.development'," + eol
    js += "    'plotlycomponent': 'https://unpkg.com/react-plotly.js@2.3/dist/create-plotly-component'," + eol
    js += "    'plotly': 'https://cdn.plot.ly/plotly-1.52.0.min'," + eol
    js += "    'math': 'https://cdnjs.cloudflare.com/ajax/libs/mathjs/6.6.1/math.min'," + eol
    js += "    'axios': 'https://unpkg.com/axios/dist/axios.min'," + eol
    js += "    'localforage' : 'https://www.unpkg.com/localforage@1.7.3/dist/localforage.min'," + eol
    js += "    'number-format': 'https://unpkg.com/react-number-format@4.3.1/dist/react-number-format'," + eol
    js += "    'prop-types': 'https://unpkg.com/prop-types@15.6/prop-types.min'" + eol
    js += "  }" + eol
    js += "});" + eol
    js += "require.undef('" + component + "')" + eol
    js += "  define('" + component + "', [" + eol
    js += "    '@jupyter-widgets/base'," + eol
    js += "    'underscore', " + eol
    js += "    'react', " + eol
    js += "    'react-dom'," + eol
    js += "    'material-ui'," + eol
    js += "    'number-format'," + eol
    js += "    'axios'," + eol
    js += "    'localforage'," + eol
    js += "    'prop-types'," + eol
    js += "    'plotlycomponent'," + eol
    js += "    'plotly'," + eol
    js += "    'math'" + eol
    js += "  ], function(" + eol
    js += "    widgets, " + eol
    js += "    _, " + eol
    js += "    React, " + eol
    js += "    ReactDOM," + eol
    js += "    Material," + eol
    js += "    Format," + eol
    js += "    Axios," + eol
    js += "    LocalForage," + eol
    js += "    PropTypes," + eol
    js += "    PlotlyComponent," + eol
    js += "    Plotly," + eol
    js += "    math" + eol
    js += "  ) {" + eol
    

    js += "    const " + component + "Model = widgets.WidgetModel.extend({}, {" + eol
    js += "        serializers: _.extend({" + eol
    for i in serializers:
        js += "            " + i + ": { deserialize: widgets.unpack_models }," + eol
    js += "        }, widgets.DOMWidgetModel.serializers)" + eol
    js += "    });" + eol
    
    js += "    const " + component + "View = widgets.DOMWidgetView.extend({" + eol
    js += "      initialize() {" + eol
    
    if (kwargs.get("debugger", False)):
        js += "        debugger;" + eol

    js += "        const backbone = this;" + eol
    js += "        widgets.DOMWidgetView.prototype.initialize.call(this, arguments);" + eol
    for i in serializers:
        js += "        backbone."+i+"_views = new widgets.ViewList(backbone.add_child_model, null, backbone);" + eol
        js += "        backbone._"+i+" = [];" + eol
        js += "        backbone."+i+"Ref = React.createRef();" + eol
    js += "        backbone.options = {};" + eol
    
    for k, v in Project.components.items():
      js += v.buildReact(k)
      js += "  " + k + ".getDerivedStateFromProps = function(props, state){" + eol
      js += "  let self = {'props':props,'state':state};" + eol
      js += "  return {" + eol
      for k1,s1 in v.stateDefinitions.items():
        v1 = s1['defaultValue']
        if isinstance(v1,dict) and "type" in v1 and v1["type"] == "dynamic":
          if ("content" in v1):
            content1 = v1["content"]
            if ("referenceType" in content1 and content1["referenceType"] == "prop"):
              v1 = "props." + content1["id"] + "";
            else:
              v1 = "state." + k1 + "";
          else:
            v1 = "state." + k1 + "";
        else:
          v1 = "state." + k1 + "";
        js += "  '" + str(k1) + "' : " + v1 + ", " + eol
      js += "  };" + eol
      js += "}" + eol

    js += Project.globals.buildReact();
    js += Project.root.buildReact(Project.root.name_component)
    js += "        const orig = " + Project.root.name_component + ".prototype.setState;" + eol
    js += "        " + Project.root.name_component + ".prototype.onChange = function (model){" + eol
    js += "          orig.apply(this, [Object.assign({},model.changed)]);" + eol
    js += "        }" + eol
    js += "        " + Project.root.name_component + ".prototype.componentDidUpdate = function(){" + eol
    for i in serializers:
        js += "          if(backbone."+i+"Ref.current){" + eol
        js += "            backbone._"+i+".forEach((e)=>{" + eol
        js += "              backbone."+i+"Ref.current.appendChild(e);" + eol
        js += "            });" + eol
        js += "          }" + eol
    js += "        }" + eol
    js += "        " + Project.root.name_component + ".getDerivedStateFromProps = function(props, state){" + eol
    js += "          return state;" + eol
    js += "        }" + eol
    js += "        " + Project.root.name_component + ".prototype.componentDidMount = function(){" + eol
    js += "          backbone.listenTo(backbone.model, 'change', this.onChange.bind(this));" + eol
    for i in serializers:
        js += "          backbone.listenTo(backbone.model, 'change:"+i+"', this.update"+i+".bind(this));" + eol
        js += "          if(backbone."+i+"Ref.current){" + eol
        js += "            this.update"+i+"(null, backbone.model.get('"+i+"'));" + eol
        js += "            backbone._"+i+".forEach((e)=>{" + eol
        js += "              backbone."+i+"Ref.current.appendChild(e);" + eol
        js += "            });" + eol
        js += "          }" + eol    
    js += "        }" + eol
    js += "        " + Project.root.name_component + ".prototype.setState = function(state, callback){" + eol
    js += parseState;
    js += "          for (let [key, value] of Object.entries(state)) {" + eol
    js += "            backbone.model.set(key, value);" + eol
    js += "          }" + eol
    js += "          backbone.model.save_changes();" + eol
    js += "          orig.apply(this, [state, callback]);" + eol
    js += "        }" + eol
    for i in serializers:   
        js += "        " + Project.root.name_component + ".prototype.update"+i+" = function(m, v){" + eol
        js += "          if (backbone."+i+"_views){" + eol
        js += "            backbone._"+i+" = [];" + eol
        js += "            backbone."+i+"_views.update(v).then((views)=>{" + eol
        js += "              views.forEach(view => {" + eol
        js += "                backbone._"+i+".push(view.el);" + eol     
        js += "              });" + eol     
        js += "              this.forceUpdate()" + eol     
        js += "            });" + eol     
        js += "          }" + eol     
        js += "        }" + eol       
    js += "        backbone.app = document.createElement('div');" + eol
    js += "        backbone.app.style.padding = '10px';" + eol
    js += "        const App = React.createElement(" + Project.root.name_component + ");" + eol
    js += "        ReactDOM.render(App, backbone.app);" + eol
    js += "        backbone.el.append(backbone.app);" + eol
    js += "      }," + eol  
    
    
    js += "      add_child_model: function(model) {" + eol
    js += "        return this.create_child_view(model).then((view) => {" + eol
    js += "          view.setLayout(view.model.get('layout'));" + eol
    js += "          let lview=view;" + eol
    js += "          lview.listenTo(lview.model,'change:layout',(m, v) => {" + eol
    js += "            this.update_children()" + eol
    js += "          });" + eol
    js += "          return view;" + eol
    js += "        });" + eol
    js += "      }, " + eol
        
    js += "      update_children: function () {" + eol
    js += "          this.children_views.update(this.model.get('children')).then(function (views) {" + eol
    js += "              views.forEach(function (view) {" + eol
    js += "                  messaging_1.MessageLoop.postMessage(view.pWidget, widgets_1.Widget.ResizeMessage.UnknownSize);" + eol
    js += "              });" + eol
    js += "          });" + eol
    js += "      }, " + eol
    
    js += "    });" + eol
    

    
    js += "    return {" + eol
    js += "      " + component + "View," + eol
    js += "      " + component + "Model" + eol
    js += "    };" + eol
    js += "});" + eol
    #out = widgets.Output()
    #display(out)
    #with out:
    #    print("DEBUG")
    def do_handle_msg(s, d, f, c, b):
        for i,j in f.items():        
            if c.get('event', '') == i:
                getattr(s,i + "_call")(s, obj=s, buf=c.get('params', ''))
                return;
        #widgets.Widget._handle_msg(s,c,b)

    def do_init(s, v, f, **k):
        widgets.DOMWidget.__init__(s,**k)
        for i,j in f.items():
            setattr(s,'_handlers_'+ i, widgets.widget.CallbackDispatcher())
            setattr(s, i , lambda c, r=False, m=i : getattr(s,'_handlers_'+ m).register_callback(c, r) )
            setattr(s, i + "_call" , lambda s, m=i, obj=s, buf=[] : getattr(s,'_handlers_'+ m)(obj=obj, buf=buf) )
            if (k.get(i,None) is not None and hasattr(k.get(i,None), '__call__')):
                getattr(s,i)(s, k.get(i,None))
        s.on_msg(lambda s1,c,b, : s1._handle_uidl_msg(c,b))
        s.__validate = True
        
        for i,j in v.items():
            setattr(s,i,k.get(i,j))
        
    def do__setattr(s,n,v,d):
        if (hasattr(s, '__validate')):
            if (n in d):
                if isinstance(d[n], str):
                    widgets.DOMWidget.__setattr__(s,n,str(v))
                elif type(d[n]) == bool:
                    widgets.DOMWidget.__setattr__(s,n,v in [True, "true", "True", "on", "yes", "Yes", "TRUE", 1, "ON"])
                elif isinstance(d[n], list):
                    widgets.DOMWidget.__setattr__(s,n,list(v))
                elif isinstance(d[n], dict):
                    vc = dict(getattr(s,n))
                    vc.update(v)
                    widgets.DOMWidget.__setattr__(s,n,vc)
                elif isinstance(d[n], int):
                    widgets.DOMWidget.__setattr__(s,n,int(v))
                elif isinstance(d[n], float):
                    widgets.DOMWidget.__setattr__(s,n,float(v))
                else :
                    widgets.DOMWidget.__setattr__(s,n,v)
            else:
                widgets.DOMWidget.__setattr__(s,n,v)

        else :
            widgets.DOMWidget.__setattr__(s,n,v)
    attrs['_model_name'] = Unicode(component + 'Model').tag(sync=True)
    attrs['_model_module'] = Unicode(component).tag(sync=True)    
    attrs['_view_name'] = Unicode(component + 'View').tag(sync=True)
    attrs['_view_module'] = Unicode(component).tag(sync=True)
    attrs['_view_module_version'] = Unicode('0.1.0').tag(sync=True)
    attrs['__init__'] =  lambda s, **k : do_init(s, default, functions, **k)
    attrs['_handle_uidl_msg'] =  lambda s,c,b, : do_handle_msg(s, default, functions, c, b)
    attrs['__setattr__'] =  lambda s,n,v, d=default : do__setattr (s,n,v,d) 

    
    default_styles = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'/>"
    display(HTML("<style>.p-Widget * {font-size: unset;}</style>"))
    display(HTML(kwargs.get("styles", default_styles)))
    if kwargs.get("verbose", False):
        print(js)
    display(Javascript(js))
                    
    return type(component + 'Widget', (widgets.DOMWidget,), attrs)

def parseJSX(document, *args, **kwargs):
    def buildNode(tag, Component):
        Node = None
        if tag.nodeType == tag.TEXT_NODE:
            if tag.data.strip() == '':
                return None
            if tag.data.strip().startswith("{") and tag.data.strip().endswith("}") :
                regex = "^\{([a-zA-Z][a-zA-Z0-9_]+)\:(.+)\((.+)\)\}$"
                m = re.match(regex,tag.data.strip())
                if m is not None:
                    state = m.group(1)
                    if (m.group(2) == "string"):
                        Component.addStateVariable(state, {"type":m.group(2), "defaultValue": m.group(3)})
                    elif m.group(2) in ["boolean", "number", "array", "object", "integer"] :
                        v = m.group(2)
                        if ( v == "integer"):
                            v = "number"
                        Component.addStateVariable(state, {"type":v, "defaultValue": json.loads(m.group(3).replace('\'','"'))})
                    else: 
                        raise Exception("not a supported type '" + m.group(2) + "'")
                    Node = TeleportDynamic(content={"referenceType": "state","id": state})

                else: 
                    raise Exception("not a supported definition" + tag.data.strip())
            else:            
                Node = TeleportStatic(content=tag.data.strip().replace("\n", "\\n"))
        else:
            if tag.tagName.startswith("Nanohub"):
                Node = TeleportElement(TeleportContent(elementType=tag.tagName.replace("Nanohub.", "")))
            elif tag.tagName.startswith("Material"):
                Node = TeleportElement(MaterialContent(elementType=tag.tagName.replace("Material.", "")))
            elif tag.tagName.startswith("Plotly"):
                Node = TeleportElement(PlotlyContent(elementType=tag.tagName.replace("Plotly.", "")))
            else:
                Node = TeleportElement(TeleportContent(elementType=tag.tagName))

            for t in tag.childNodes:
                node = buildNode(t, Component)
                if node is not None:
                    Node.addContent(node)
        if (tag.attributes is not None):
            for k,v in tag.attributes.items():
                if v.startswith("{") and v.endswith("}") :
                    regex = "^\{([a-zA-Z][a-zA-Z0-9_]+)\:(.+)\((.+)\)\}$"
                    m = re.match(regex,v)
                    if m is not None:
                        state = m.group(1)
                        if k=="_children": 
                            if (m.group(2) == "array"):
                                Component.addStateVariable(state, {"type":"router", "defaultValue": []})
                                Node.content.attrs['ref']={
                                  "type": "dynamic",
                                  "content": {
                                    "referenceType": "local",
                                    "id": 'backbone.' + state + 'Ref'
                                  }    
                                }  
                                Node.content.attrs[k]=''
                            else:
                                raise Exception("_children only support array type'" + m.group(2) + "'")
                        else :
                            if (m.group(2) == "string"):
                                Component.addStateVariable(state, {"type":m.group(2), "defaultValue": m.group(3)})
                            elif m.group(2) in ["boolean", "number", "array", "object", "integer"] :
                                v = m.group(2)
                                if ( v == "integer"):
                                    v = "number"
                                Component.addStateVariable(state, {"type":m.group(2), "defaultValue": json.loads(m.group(3).replace('\'','"'))})
                            else: 
                                raise Exception("not a supported type '" + m.group(2) + "'")
                        Node.content.attrs[k]={
                          "type": "dynamic",
                          "content": {
                            "referenceType": "state",
                            "id": state
                          }    
                        }
                    else: 
                        raise Exception("not a supported definition" + v)

                elif v.startswith("[") and v.endswith("]") :
                    regex = "^\[([a-zA-Z][a-zA-Z0-9]+)\((.+),(.+)\)\]$"
                    m = re.match(regex,v)
                    if m is not None:
                        if m.group(1) in ["stateChange"]:
                            Component.addPropVariable(k, {"type":"func", "defaultValue": "(e)=>{return e; }"})
                            Component.addPropVariable("onChange", {"type":"func", "defaultValue": "(e)=>{return e; }"})
                            v = m.group(3)
                            if v == "$toogle":
                                v = "!self.state." + m.group(2)
                            Node.content.events[k] = [
                                {
                                    "type": m.group(1),
                                    "modifies": m.group(2),
                                    "newState": '$'+v,
                                },
                                {
                                    "type": "propCall2",
                                    "calls": 'onChange',
                                    "args": ["{'id':'"+m.group(2)+"', 'value':" + v + "}"]
                                }
                            ]
                        elif m.group(1) in ["propCall", "propCall2"]:
                            Component.addPropVariable(m.group(2), {"type":"func", "defaultValue": "(e)=>{return e; }"})
                            Node.content.events[k] = [
                                {
                                    "type": "propCall2",
                                    "calls": m.group(2),
                                    "args": [m.group(3)]
                                },
                            ]
                        else: 
                            raise Exception("not a supported function" + m.group(1))
                    else: 
                        raise Exception("not a valid function" + v)
                elif k=="style": 
                    Node.content.style = { a[0] : a[1] for a in [t.split(":") for t in v.split(";")] }
                else:
                    Node.content.attrs[k]=v

        return Node
    document = "<uidl>" + document + "</uidl>"
    dom = xml.dom.minidom.parseString(document)
    component = kwargs.get("component_name", str(uuid.uuid4()) )
    component = "UIDL" + component.replace("-","")    
    Component = TeleportComponent(component, TeleportElement(MaterialContent(elementType="Paper")));

    for node in dom.childNodes[0].childNodes:
        if node.nodeType != node.TEXT_NODE:
            Component.node.addContent(buildNode(node, Component))    
    return Component;    
    
def buildJSX(document, *args, **kwargs):
    component = kwargs.get("component_name", str(uuid.uuid4()) )
    component = "UIDL" + component.replace("-","")
    Component = parseJSX(document, *args, **kwargs)
    Project = TeleportProject(component, content=Component)
    Project.root.propDefinitions = Component.propDefinitions
    Project.root.stateDefinitions = Component.stateDefinitions
    Project.root.node = Component.node
    for t in Component.getNodeTypes():
        if t == "FormatCustomNumber":
            MaterialComponents.FormatCustomNumber(Project)
        elif t == "IconListMaterial":
            MaterialComponents.IconList(Project)
        elif t == "IntSwitch":
            MaterialComponents.IntSwitch(Project)    
        elif t == "ButtonListMaterial":
            MaterialComponents.ButtonList(Project)  
        elif t == "ColorSliders":
            MaterialComponents.ColorSliders(Project)  
    
    if kwargs.get("verbose", False):
        print(Project.root.buildReact(component))
    return buildWidget(Project, **kwargs);