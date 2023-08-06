"use strict";define(["tvguide"],(function(tvguide){return function(view,params,tabContent){var guideInstance;this.renderTab=function(){guideInstance||(guideInstance=new tvguide({element:tabContent,serverId:ApiClient.serverId()}))},this.onShow=function(){guideInstance&&guideInstance.resume()},this.onHide=function(){guideInstance&&guideInstance.pause()}}}));
//# sourceMappingURL=livetvguide.js.map
