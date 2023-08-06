(self.webpackJsonp=self.webpackJsonp||[]).push([[216],{364:function(e,t,i){"use strict";var r=i(70);i.d(t,"a",function(){return n}),i.d(t,"b",function(){return a}),i.d(t,"e",function(){return o}),i.d(t,"d",function(){return c}),i.d(t,"c",function(){return l}),i.d(t,"f",function(){return d});const n=2,a=e=>`/api/camera_proxy_stream/${e.entity_id}?token=${e.attributes.access_token}`,o=(e,t)=>(async(e,t,i,r,n,...a)=>{let o=r[e];o||(o=r[e]={});const s=o[n];if(s)return s;const c=i(r,n,...a);return o[n]=c,c.then(()=>setTimeout(()=>{o[n]=void 0},t),()=>{o[n]=void 0}),c})("_cameraTmbUrl",9e3,s,e,t),s=async(e,t)=>{const i=await Object(r.b)(e,`/api/camera_proxy/${t}`);return e.hassUrl(i.path)},c=async(e,t,i)=>{const r={type:"camera/stream",entity_id:t};i&&(r.format=i);const n=await e.callWS(r);return n.url=e.hassUrl(n.url),n},l=(e,t)=>e.callWS({type:"camera/get_prefs",entity_id:t}),d=(e,t,i)=>e.callWS(Object.assign({type:"camera/update_prefs",entity_id:t},i))},400:function(e,t,i){"use strict";i.d(t,"a",function(){return n});const r=e=>{const t=parseFloat(e);if(isNaN(t))throw new Error(`${e} is not a number`);return t};function n(e){if(!e)return null;try{if(e.endsWith("%"))return{w:100,h:r(e.substr(0,e.length-1))};const i=e.replace(":","x").split("x");return 0===i.length?null:1===i.length?{w:r(i[0]),h:1}:{w:r(i[0]),h:r(i[1])}}catch(t){}return null}},439:function(e,t,i){"use strict";var r=i(190),n=i(400),a=i(0),o=i(234),s=i(69),c=i(364);function l(e){var t,i=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var a="static"===n?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[a])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=p(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=u(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var a=0;a<r.length;a++)n=r[a](n);var o=t(function(e){n.initializeInstanceElements(e,s.elements)},i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var n,a=e[r];if("method"===a.kind&&(n=t.find(i)))if(f(a.descriptor)||f(n.descriptor)){if(h(a)||h(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(h(a)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}d(a,n)}else t.push(a)}return t}(o.d.map(l)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([Object(a.d)("hui-image")],function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(a.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"entity",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"image",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"stateImage",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"cameraImage",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"cameraView",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"aspectRatio",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"filter",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"stateFilter",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"_loadError",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"_cameraImageSrc",value:void 0},{kind:"field",decorators:[Object(a.h)("img")],key:"_image",value:void 0},{kind:"field",key:"_lastImageHeight",value:void 0},{kind:"field",key:"_cameraUpdater",value:void 0},{kind:"field",key:"_attached",value:void 0},{kind:"method",key:"connectedCallback",value:function(){m(g(i.prototype),"connectedCallback",this).call(this),this._attached=!0,this.cameraImage&&"live"!==this.cameraView&&this._startUpdateCameraInterval()}},{kind:"method",key:"disconnectedCallback",value:function(){m(g(i.prototype),"disconnectedCallback",this).call(this),this._attached=!1,this._stopUpdateCameraInterval()}},{kind:"method",key:"render",value:function(){const e=this.aspectRatio?Object(n.a)(this.aspectRatio):null,t=this.hass&&this.entity?this.hass.states[this.entity]:void 0,i=t?t.state:"unavailable";let c,l,d=!this.stateImage;if(this.cameraImage)"live"===this.cameraView?l=this.hass&&this.hass.states[this.cameraImage]:c=this._cameraImageSrc;else if(this.stateImage){const e=this.stateImage[i];e?c=e:(c=this.image,d=!0)}else c=this.image;c&&(c=this.hass.hassUrl(c));let h=this.filter||"";if(this.stateFilter&&this.stateFilter[i]&&(h=this.stateFilter[i]),!h&&this.entity){h=(!t||r.h.includes(i))&&d?"grayscale(100%)":""}return a.f`
      <div
        style=${Object(o.a)({paddingBottom:e&&e.w>0&&e.h>0?`${(100*e.h/e.w).toFixed(2)}%`:""})}
        class=${Object(s.a)({ratio:Boolean(e&&e.w>0&&e.h>0)})}
      >
        ${this.cameraImage&&"live"===this.cameraView?a.f`
              <ha-camera-stream
                .hass=${this.hass}
                .stateObj="${l}"
              ></ha-camera-stream>
            `:a.f`
              <img
                id="image"
                src=${c}
                @error=${this._onImageError}
                @load=${this._onImageLoad}
                style=${Object(o.a)({filter:h,display:this._loadError?"none":"block"})}
              />
            `}
        <div
          id="brokenImage"
          style=${Object(o.a)({height:`${this._lastImageHeight||"100"}px`,display:this._loadError?"block":"none"})}
        ></div>
      </div>
    `}},{kind:"method",key:"updated",value:function(e){if(e.has("cameraImage")&&"live"!==this.cameraView)return this._updateCameraImageSrc(),void this._startUpdateCameraInterval()}},{kind:"method",key:"_startUpdateCameraInterval",value:function(){this._stopUpdateCameraInterval(),this.cameraImage&&this._attached&&(this._cameraUpdater=window.setInterval(()=>this._updateCameraImageSrc(),1e4))}},{kind:"method",key:"_stopUpdateCameraInterval",value:function(){this._cameraUpdater&&clearInterval(this._cameraUpdater)}},{kind:"method",key:"_onImageError",value:function(){this._loadError=!0}},{kind:"method",key:"_onImageLoad",value:async function(){this._loadError=!1,await this.updateComplete,this._lastImageHeight=this._image.offsetHeight}},{kind:"method",key:"_updateCameraImageSrc",value:async function(){if(!this.hass||!this.cameraImage)return;this.hass.states[this.cameraImage]?this._cameraImageSrc=await Object(c.e)(this.hass,this.cameraImage):this._onImageError()}},{kind:"get",static:!0,key:"styles",value:function(){return a.c`
      img {
        display: block;
        height: auto;
        transition: filter 0.2s linear;
        width: 100%;
      }

      .ratio {
        position: relative;
        width: 100%;
        height: 0;
      }

      .ratio img,
      .ratio div {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }

      #brokenImage {
        background: grey url("/static/images/image-broken.svg") center/36px
          no-repeat;
      }
    `}}]}},a.a)},70:function(e,t,i){"use strict";i.d(t,"c",function(){return r}),i.d(t,"b",function(){return n}),i.d(t,"a",function(){return a});const r=`${location.protocol}//${location.host}`,n=(e,t)=>e.callWS({type:"auth/sign_path",path:t}),a=()=>fetch("/auth/providers",{credentials:"same-origin"})},838:function(e,t,i){"use strict";i.r(t);var r=i(0),n=i(69),a=i(200),o=(i(187),i(189),i(439),i(356),i(188)),s=i(131),c=i(208),l=i(259),d=i(190),h=i(292),f=i(218),u=i(111),p=i(246),m=i(268),g=i(269),y=i(256);function v(e){var t,i=E(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function b(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function k(e){return e.decorators&&e.decorators.length}function w(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function E(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function O(e,t,i){return(O="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=j(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function j(e){return(j=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const x=new Set(["closed","locked","not_home","off"]);!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var a="static"===n?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!k(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[a])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=E(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=_(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=_(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var a=0;a<r.length;a++)n=r[a](n);var o=t(function(e){n.initializeInstanceElements(e,s.elements)},i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var n,a=e[r];if("method"===a.kind&&(n=t.find(i)))if(w(a.descriptor)||w(n.descriptor)){if(k(a)||k(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(k(a)){if(k(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}b(a,n)}else t.push(a)}return t}(o.d.map(v)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([Object(r.d)("hui-picture-glance-card")],function(e,t){class v extends t{constructor(...t){super(...t),e(this)}}return{F:v,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([i.e(0),i.e(1),i.e(3),i.e(4),i.e(79)]).then(i.bind(null,793)),document.createElement("hui-picture-glance-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i,r){return{type:"picture-glance",title:"Kitchen",image:"https://demo.home-assistant.io/stub_config/kitchen.png",entities:Object(y.a)(e,t,2,i,r,["sensor","binary_sensor"])}}},{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_config",value:void 0},{kind:"field",key:"_entitiesDialog",value:void 0},{kind:"field",key:"_entitiesToggle",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(!e||!e.entities||!Array.isArray(e.entities)||!(e.image||e.camera_image||e.state_image)||e.state_image&&!e.entity)throw new Error("Invalid card configuration");const t=Object(h.a)(e.entities);this._entitiesDialog=[],this._entitiesToggle=[],t.forEach(t=>{e.force_dialog||!d.e.has(Object(s.a)(t.entity))?this._entitiesDialog.push(t):this._entitiesToggle.push(t)}),this._config=e}},{kind:"method",key:"shouldUpdate",value:function(e){if(Object(f.a)(this,e))return!0;const t=e.get("hass");if(!t||t.themes!==this.hass.themes||t.language!==this.hass.language)return!0;if(this._entitiesDialog)for(const i of this._entitiesDialog)if(t.states[i.entity]!==this.hass.states[i.entity])return!0;if(this._entitiesToggle)for(const i of this._entitiesToggle)if(t.states[i.entity]!==this.hass.states[i.entity])return!0;return!1}},{kind:"method",key:"updated",value:function(e){if(O(j(v.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),i=e.get("_config");t&&i&&t.themes===this.hass.themes&&i.theme===this._config.theme||Object(u.a)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?r.f`
      <ha-card>
        <hui-image
          class=${Object(n.a)({clickable:Boolean(this._config.tap_action||this._config.hold_action||this._config.camera_image)})}
          @action=${this._handleAction}
          .actionHandler=${Object(p.a)({hasHold:Object(m.a)(this._config.hold_action),hasDoubleClick:Object(m.a)(this._config.double_tap_action)})}
          tabindex=${Object(a.a)(Object(m.a)(this._config.tap_action)?"0":void 0)}
          .config=${this._config}
          .hass=${this.hass}
          .image=${this._config.image}
          .stateImage=${this._config.state_image}
          .stateFilter=${this._config.state_filter}
          .cameraImage=${this._config.camera_image}
          .cameraView=${this._config.camera_view}
          .entity=${this._config.entity}
          .aspectRatio=${this._config.aspect_ratio}
        ></hui-image>
        <div class="box">
          ${this._config.title?r.f`
                <div class="title">${this._config.title}</div>
              `:""}
          <div class="row">
            ${this._entitiesDialog.map(e=>this.renderEntity(e,!0))}
          </div>
          <div class="row">
            ${this._entitiesToggle.map(e=>this.renderEntity(e,!1))}
          </div>
        </div>
      </ha-card>
    `:r.f``}},{kind:"method",key:"renderEntity",value:function(e,t){const i=this.hass.states[e.entity];return e=Object.assign({tap_action:{action:t?"more-info":"toggle"}},e),i?r.f`
      <div class="wrapper">
        <ha-icon
          @action=${this._handleAction}
          .actionHandler=${Object(p.a)({hasHold:Object(m.a)(e.hold_action),hasDoubleClick:Object(m.a)(e.double_tap_action)})}
          tabindex=${Object(a.a)(Object(m.a)(e.tap_action)?"0":void 0)}
          .config=${e}
          class="${Object(n.a)({"state-on":!x.has(i.state)})}"
          .icon="${e.icon||Object(c.a)(i)}"
          title="${`\n            ${Object(o.a)(i)} : ${Object(l.a)(this.hass.localize,i,this.hass.language)}\n          `}"
        ></ha-icon>
        ${!0!==this._config.show_state&&!0!==e.show_state?r.f`
              <div class="state"></div>
            `:r.f`
              <div class="state">
                ${e.attribute?r.f`
                      ${e.prefix}${i.attributes[e.attribute]}${e.suffix}
                    `:Object(l.a)(this.hass.localize,i,this.hass.language)}
              </div>
            `}
      </div>
    `:r.f`
        <hui-warning-element
          label=${this.hass.localize("ui.panel.lovelace.warning.entity_not_found","entity",e.entity)}
        ></hui-warning-element>
      `}},{kind:"method",key:"_handleAction",value:function(e){const t=e.currentTarget.config;Object(g.a)(this,this.hass,t,e.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      ha-card {
        position: relative;
        min-height: 48px;
        overflow: hidden;
      }

      hui-image.clickable {
        cursor: pointer;
      }

      .box {
        /* start paper-font-common-nowrap style */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        /* end paper-font-common-nowrap style */

        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.3);
        padding: 4px 8px;
        font-size: 16px;
        line-height: 40px;
        color: white;
        display: flex;
        justify-content: space-between;
        flex-direction: row;
      }

      .box .title {
        font-weight: 500;
        margin-left: 8px;
      }

      ha-icon {
        cursor: pointer;
        padding: 8px;
        color: #a9a9a9;
      }

      ha-icon.state-on {
        color: white;
      }
      ha-icon.show-state {
        width: 20px;
        height: 20px;
        padding-bottom: 4px;
        padding-top: 4px;
      }
      ha-icon:focus {
        outline: none;
        background: var(--divider-color);
        border-radius: 100%;
      }
      .state {
        display: block;
        font-size: 12px;
        text-align: center;
        line-height: 12px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .row {
        display: flex;
        flex-direction: row;
      }
      .wrapper {
        display: flex;
        flex-direction: column;
        width: 40px;
      }
    `}}]}},r.a)}}]);
//# sourceMappingURL=chunk.bc5b1f932e2ef167121a.js.map