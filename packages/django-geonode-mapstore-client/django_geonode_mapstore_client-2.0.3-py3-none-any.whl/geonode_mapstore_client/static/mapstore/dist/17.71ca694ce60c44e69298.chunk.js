(window.webpackJsonp=window.webpackJsonp||[]).push([[17],{2240:function(e,t,n){var i=n(2319),r=i.OWS_1_0_0,l=i.DCT,a=i.SMIL_2_0,o=i.SMIL_2_0_Language,s=i.GML_3_1_1,m=i.Filter_1_1_0,p=i.CSW_2_0_2,c=i.GML_3_2_0,_=i.GML_3_2_1,S=i.ISO19139_GCO_20070417,w=i.ISO19139_GMD_20070417,u=i.ISO19139_GMX_20070417,h=i.ISO19139_GSS_20070417,g=i.ISO19139_GTS_20070417,C=i.ISO19139_GSR_20070417,d=i.ISO19139_2_GMI_1_0,y=n(2558),L=n(2320).XLink_1_0,D=new(n(2321).Jsonix.Context)([r,y,l,L,a,o,s,m,p,c,_,S,w,u,h,g,C,d],{namespacePrefixes:{"http://www.opengis.net/cat/csw/2.0.2":"csw","http://www.opengis.net/ogc":"ogc","http://www.opengis.net/gml":"gml","http://purl.org/dc/elements/1.1/":"dc","http://purl.org/dc/terms/":"dct","http://www.isotc211.org/2005/gmd":"gmd","http://www.isotc211.org/2005/gco":"gco","http://www.isotc211.org/2005/gmi":"gmi","http://www.opengis.net/ows":"ows"}}),I=D.createMarshaller(),f=D.createUnmarshaller(),v={getRecords:function(e,t,n,i){var r={startPosition:e,maxRecords:t,abstractQuery:v.query("full",n&&v.constraint(n)),resultType:"results",service:"CSW",version:"2.0.2"};return i&&(r.outputSchema=i),r},getRecordById:function(e){return{TYPE_NAME:"CSW_2_0_2.GetRecordByIdType",elementSetName:{ObjectTYPE_NAME:"CSW_2_0_2.ElementSetNameType",value:"full"},id:Array.isArray(e)?e:[e],service:"CSW",version:"2.0.2"}},query:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"full",t=arguments.length>1?arguments[1]:void 0,n={"csw:Query":{TYPE_NAME:"CSW_2_0_2.QueryType",elementSetName:{TYPE_NAME:"CSW_2_0_2.ElementSetNameType",value:e},typeNames:[{key:"{http://www.opengis.net/cat/csw/2.0.2}Record",localPart:"Record",namespaceURI:"http://www.opengis.net/cat/csw/2.0.2",prefix:"csw",string:"{http://www.opengis.net/cat/csw/2.0.2}csw:Record"}]}};return t&&(n["csw:Query"].constraint=t),n},constraint:function(e){return{TYPE_NAME:"CSW_2_0_2.QueryConstraintType",version:"1.1.0",filter:e}}};e.exports={CSW:v,marshaller:I,unmarshaller:f}},2558:function(e,t){e.exports={n:"DC_1_1",dens:"http://purl.org/dc/elements/1.1/",tis:[{ln:"ElementContainer",tn:"elementContainer",ps:[{n:"dcElement",mno:0,col:!0,mx:!1,dom:!1,en:"DC-element",ti:".SimpleLiteral",t:"er"},{n:"dcElement",mno:0,col:!0,mx:!1,dom:!1,en:"DC-element",ti:".URI",t:"er"}]},{ln:"SimpleLiteral",ps:[{n:"content",col:!0,dom:!1,t:"ers"},{n:"scheme",an:{lp:"scheme"},t:"a"}]},{ln:"URI",ti:"URI",sh:"DC-element",collection:!0,propertyInfos:[{type:"attribute",name:"name",attributeName:"name",typeInfo:"String"},{type:"attribute",name:"description",attributeName:"description",typeInfo:"String"},{type:"attribute",name:"protocol",attributeName:"protocol",typeInfo:"String"},{type:"value",name:"value",typeInfo:"String"}]}],eis:[{en:"identifier",ti:".SimpleLiteral",sh:"DC-element"},{en:"relation",ti:".SimpleLiteral",sh:"DC-element"},{en:"format",ti:".SimpleLiteral",sh:"DC-element"},{en:"title",ti:".SimpleLiteral",sh:"DC-element"},{en:"description",ti:".SimpleLiteral",sh:"DC-element"},{en:"source",ti:".SimpleLiteral",sh:"DC-element"},{en:"date",ti:".SimpleLiteral",sh:"DC-element"},{en:"type",ti:".SimpleLiteral",sh:"DC-element"},{en:"language",ti:".SimpleLiteral",sh:"DC-element"},{en:"DC-element",ti:".SimpleLiteral"},{en:"rights",ti:".SimpleLiteral",sh:"DC-element"},{en:"creator",ti:".SimpleLiteral",sh:"DC-element"},{en:"publisher",ti:".SimpleLiteral",sh:"DC-element"},{en:"contributor",ti:".SimpleLiteral",sh:"DC-element"},{en:"subject",ti:".SimpleLiteral",sh:"DC-element"},{en:"coverage",ti:".SimpleLiteral",sh:"DC-element"},{en:"URI",ti:".URI",sh:"DC-element"}]}}}]);