/*! For license information please see chunk.9cb9e16821a19528b908.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[240],{847:function(t,e,i){(function(t){(function(){"use strict";const e=new WeakMap,i=t=>(...i)=>{const r=t(...i);return e.set(r,!0),r},r=t=>"function"==typeof t&&e.has(t),s=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,o=(t,e,i=null)=>{for(;e!==i;){const i=e.nextSibling;t.removeChild(e),e=i}},n={},a={},c=`{{lit-${String(Math.random()).slice(2)}}}`,l=`\x3c!--${c}--\x3e`,p=new RegExp(`${c}|${l}`),h="$lit$";class d{constructor(t,e){this.parts=[],this.element=e;const i=[],r=[],s=document.createTreeWalker(e.content,133,null,!1);let o=0,n=-1,a=0;const{strings:l,values:{length:d}}=t;for(;a<d;){const t=s.nextNode();if(null!==t){if(n++,1===t.nodeType){if(t.hasAttributes()){const e=t.attributes,{length:i}=e;let r=0;for(let t=0;t<i;t++)u(e[t].name,h)&&r++;for(;r-- >0;){const e=l[a],i=f.exec(e)[2],r=i.toLowerCase()+h,s=t.getAttribute(r);t.removeAttribute(r);const o=s.split(p);this.parts.push({type:"attribute",index:n,name:i,strings:o}),a+=o.length-1}}"TEMPLATE"===t.tagName&&(r.push(t),s.currentNode=t.content)}else if(3===t.nodeType){const e=t.data;if(e.indexOf(c)>=0){const r=t.parentNode,s=e.split(p),o=s.length-1;for(let e=0;e<o;e++){let i,o=s[e];if(""===o)i=g();else{const t=f.exec(o);null!==t&&u(t[2],h)&&(o=o.slice(0,t.index)+t[1]+t[2].slice(0,-h.length)+t[3]),i=document.createTextNode(o)}r.insertBefore(i,t),this.parts.push({type:"node",index:++n})}""===s[o]?(r.insertBefore(g(),t),i.push(t)):t.data=s[o],a+=o}}else if(8===t.nodeType)if(t.data===c){const e=t.parentNode;null!==t.previousSibling&&n!==o||(n++,e.insertBefore(g(),t)),o=n,this.parts.push({type:"node",index:n}),null===t.nextSibling?t.data="":(i.push(t),n--),a++}else{let e=-1;for(;-1!==(e=t.data.indexOf(c,e+1));)this.parts.push({type:"node",index:-1}),a++}}else s.currentNode=r.pop()}for(const c of i)c.parentNode.removeChild(c)}}const u=(t,e)=>{const i=t.length-e.length;return i>=0&&t.slice(i)===e},m=t=>-1!==t.index,g=()=>document.createComment(""),f=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=\/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/;class _{constructor(t,e,i){this.__parts=[],this.template=t,this.processor=e,this.options=i}update(t){let e=0;for(const i of this.__parts)void 0!==i&&i.setValue(t[e]),e++;for(const i of this.__parts)void 0!==i&&i.commit()}_clone(){const t=s?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),e=[],i=this.template.parts,r=document.createTreeWalker(t,133,null,!1);let o,n=0,a=0,c=r.nextNode();for(;n<i.length;)if(o=i[n],m(o)){for(;a<o.index;)a++,"TEMPLATE"===c.nodeName&&(e.push(c),r.currentNode=c.content),null===(c=r.nextNode())&&(r.currentNode=e.pop(),c=r.nextNode());if("node"===o.type){const t=this.processor.handleTextExpression(this.options);t.insertAfterNode(c.previousSibling),this.__parts.push(t)}else this.__parts.push(...this.processor.handleAttributeExpressions(c,o.name,o.strings,this.options));n++}else this.__parts.push(void 0),n++;return s&&(document.adoptNode(t),customElements.upgrade(t)),t}}const v=` ${c} `;class y{constructor(t,e,i,r){this.strings=t,this.values=e,this.type=i,this.processor=r}getHTML(){const t=this.strings.length-1;let e="",i=!1;for(let r=0;r<t;r++){const t=this.strings[r],s=t.lastIndexOf("\x3c!--");i=(s>-1||i)&&-1===t.indexOf("--\x3e",s+1);const o=f.exec(t);e+=null===o?t+(i?v:l):t.substr(0,o.index)+o[1]+o[2]+h+o[3]+c}return e+=this.strings[t]}getTemplateElement(){const t=document.createElement("template");return t.innerHTML=this.getHTML(),t}}const b=t=>null===t||!("object"==typeof t||"function"==typeof t),w=t=>Array.isArray(t)||!(!t||!t[Symbol.iterator]);class x{constructor(t,e,i){this.dirty=!0,this.element=t,this.name=e,this.strings=i,this.parts=[];for(let r=0;r<i.length-1;r++)this.parts[r]=this._createPart()}_createPart(){return new k(this)}_getValue(){const t=this.strings,e=t.length-1;let i="";for(let r=0;r<e;r++){i+=t[r];const e=this.parts[r];if(void 0!==e){const t=e.value;if(b(t)||!w(t))i+="string"==typeof t?t:String(t);else for(const e of t)i+="string"==typeof e?e:String(e)}}return i+=t[e]}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class k{constructor(t){this.value=void 0,this.committer=t}setValue(t){t===n||b(t)&&t===this.value||(this.value=t,r(t)||(this.committer.dirty=!0))}commit(){for(;r(this.value);){const t=this.value;this.value=n,t(this)}this.value!==n&&this.committer.commit()}}class S{constructor(t){this.value=void 0,this.__pendingValue=void 0,this.options=t}appendInto(t){this.startNode=t.appendChild(g()),this.endNode=t.appendChild(g())}insertAfterNode(t){this.startNode=t,this.endNode=t.nextSibling}appendIntoPart(t){t.__insert(this.startNode=g()),t.__insert(this.endNode=g())}insertAfterPart(t){t.__insert(this.startNode=g()),this.endNode=t.endNode,t.endNode=this.startNode}setValue(t){this.__pendingValue=t}commit(){for(;r(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=n,t(this)}const t=this.__pendingValue;t!==n&&(b(t)?t!==this.value&&this.__commitText(t):t instanceof y?this.__commitTemplateResult(t):t instanceof Node?this.__commitNode(t):w(t)?this.__commitIterable(t):t===a?(this.value=a,this.clear()):this.__commitText(t))}__insert(t){this.endNode.parentNode.insertBefore(t,this.endNode)}__commitNode(t){this.value!==t&&(this.clear(),this.__insert(t),this.value=t)}__commitText(t){const e=this.startNode.nextSibling,i="string"==typeof(t=null==t?"":t)?t:String(t);e===this.endNode.previousSibling&&3===e.nodeType?e.data=i:this.__commitNode(document.createTextNode(i)),this.value=t}__commitTemplateResult(t){const e=this.options.templateFactory(t);if(this.value instanceof _&&this.value.template===e)this.value.update(t.values);else{const i=new _(e,t.processor,this.options),r=i._clone();i.update(t.values),this.__commitNode(r),this.value=i}}__commitIterable(t){Array.isArray(this.value)||(this.value=[],this.clear());const e=this.value;let i,r=0;for(const s of t)void 0===(i=e[r])&&(i=new S(this.options),e.push(i),0===r?i.appendIntoPart(this):i.insertAfterPart(e[r-1])),i.setValue(s),i.commit(),r++;r<e.length&&(e.length=r,this.clear(i&&i.endNode))}clear(t=this.startNode){o(this.startNode.parentNode,t.nextSibling,this.endNode)}}class ${constructor(t,e,i){if(this.value=void 0,this.__pendingValue=void 0,2!==i.length||""!==i[0]||""!==i[1])throw new Error("Boolean attributes can only contain a single expression");this.element=t,this.name=e,this.strings=i}setValue(t){this.__pendingValue=t}commit(){for(;r(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=n,t(this)}if(this.__pendingValue===n)return;const t=!!this.__pendingValue;this.value!==t&&(t?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name),this.value=t),this.__pendingValue=n}}class P extends x{constructor(t,e,i){super(t,e,i),this.single=2===i.length&&""===i[0]&&""===i[1]}_createPart(){return new E(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class E extends k{}let C=!1;try{const t={get capture(){return C=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(Zt){}class O{constructor(t,e,i){this.value=void 0,this.__pendingValue=void 0,this.element=t,this.eventName=e,this.eventContext=i,this.__boundHandleEvent=(t=>this.handleEvent(t))}setValue(t){this.__pendingValue=t}commit(){for(;r(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=n,t(this)}if(this.__pendingValue===n)return;const t=this.__pendingValue,e=this.value,i=null==t||null!=e&&(t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive),s=null!=t&&(null==e||i);i&&this.element.removeEventListener(this.eventName,this.__boundHandleEvent,this.__options),s&&(this.__options=A(t),this.element.addEventListener(this.eventName,this.__boundHandleEvent,this.__options)),this.value=t,this.__pendingValue=n}handleEvent(t){"function"==typeof this.value?this.value.call(this.eventContext||this.element,t):this.value.handleEvent(t)}}const A=t=>t&&(C?{capture:t.capture,passive:t.passive,once:t.once}:t.capture),T=new class{handleAttributeExpressions(t,e,i,r){const s=e[0];return"."===s?new P(t,e.slice(1),i).parts:"@"===s?[new O(t,e.slice(1),r.eventContext)]:"?"===s?[new $(t,e.slice(1),i)]:new x(t,e,i).parts}handleTextExpression(t){return new S(t)}};function N(t){let e=M.get(t.type);void 0===e&&(e={stringsArray:new WeakMap,keyString:new Map},M.set(t.type,e));let i=e.stringsArray.get(t.strings);if(void 0!==i)return i;const r=t.strings.join(c);return void 0===(i=e.keyString.get(r))&&(i=new d(t,t.getTemplateElement()),e.keyString.set(r,i)),e.stringsArray.set(t.strings,i),i}const M=new Map,V=new WeakMap;(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.1.2");const z=(t,...e)=>new y(t,e,"html",T),R=133;function j(t,e){const{element:{content:i},parts:r}=t,s=document.createTreeWalker(i,R,null,!1);let o=B(r),n=r[o],a=-1,c=0;const l=[];let p=null;for(;s.nextNode();){a++;const t=s.currentNode;for(t.previousSibling===p&&(p=null),e.has(t)&&(l.push(t),null===p&&(p=t)),null!==p&&c++;void 0!==n&&n.index===a;)n.index=null!==p?-1:n.index-c,n=r[o=B(r,o)]}l.forEach(t=>t.parentNode.removeChild(t))}const L=t=>{let e=11===t.nodeType?0:1;const i=document.createTreeWalker(t,R,null,!1);for(;i.nextNode();)e++;return e},B=(t,e=-1)=>{for(let i=e+1;i<t.length;i++){const e=t[i];if(m(e))return i}return-1},U=(t,e)=>`${t}--${e}`;let I=!0;void 0===window.ShadyCSS?I=!1:void 0===window.ShadyCSS.prepareTemplateDom&&(console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."),I=!1);const W=t=>e=>{const i=U(e.type,t);let r=M.get(i);void 0===r&&(r={stringsArray:new WeakMap,keyString:new Map},M.set(i,r));let s=r.stringsArray.get(e.strings);if(void 0!==s)return s;const o=e.strings.join(c);if(void 0===(s=r.keyString.get(o))){const i=e.getTemplateElement();I&&window.ShadyCSS.prepareTemplateDom(i,t),s=new d(e,i),r.keyString.set(o,s)}return r.stringsArray.set(e.strings,s),s},D=["html","svg"],q=new Set,H=(t,e,i)=>{q.add(t);const r=i?i.element:document.createElement("template"),s=e.querySelectorAll("style"),{length:o}=s;if(0===o)return void window.ShadyCSS.prepareTemplateStyles(r,t);const n=document.createElement("style");for(let l=0;l<o;l++){const t=s[l];t.parentNode.removeChild(t),n.textContent+=t.textContent}(t=>{D.forEach(e=>{const i=M.get(U(e,t));void 0!==i&&i.keyString.forEach(t=>{const{element:{content:e}}=t,i=new Set;Array.from(e.querySelectorAll("style")).forEach(t=>{i.add(t)}),j(t,i)})})})(t);const a=r.content;i?function(t,e,i=null){const{element:{content:r},parts:s}=t;if(null==i)return void r.appendChild(e);const o=document.createTreeWalker(r,R,null,!1);let n=B(s),a=0,c=-1;for(;o.nextNode();)for(c++,o.currentNode===i&&(a=L(e),i.parentNode.insertBefore(e,i));-1!==n&&s[n].index===c;){if(a>0){for(;-1!==n;)s[n].index+=a,n=B(s,n);return}n=B(s,n)}}(i,n,a.firstChild):a.insertBefore(n,a.firstChild),window.ShadyCSS.prepareTemplateStyles(r,t);const c=a.querySelector("style");if(window.ShadyCSS.nativeShadow&&null!==c)e.insertBefore(c.cloneNode(!0),e.firstChild);else if(i){a.insertBefore(n,a.firstChild);const t=new Set;t.add(n),j(i,t)}};window.JSCompiler_renameProperty=((t,e)=>t);const F={toAttribute(t,e){switch(e){case Boolean:return t?"":null;case Object:case Array:return null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){switch(e){case Boolean:return null!==t;case Number:return null===t?null:Number(t);case Object:case Array:return JSON.parse(t)}return t}},G=(t,e)=>e!==t&&(e==e||t==t),X={attribute:!0,type:String,converter:F,reflect:!1,hasChanged:G},J=Promise.resolve(!0),Z=1,Y=4,K=8,Q=16,tt=32,et="finalized";class it extends HTMLElement{constructor(){super(),this._updateState=0,this._instanceProperties=void 0,this._updatePromise=J,this._hasConnectedResolver=void 0,this._changedProperties=new Map,this._reflectingProperties=void 0,this.initialize()}static get observedAttributes(){this.finalize();const t=[];return this._classProperties.forEach((e,i)=>{const r=this._attributeNameForProperty(i,e);void 0!==r&&(this._attributeToPropertyMap.set(r,i),t.push(r))}),t}static _ensureClassProperties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties",this))){this._classProperties=new Map;const t=Object.getPrototypeOf(this)._classProperties;void 0!==t&&t.forEach((t,e)=>this._classProperties.set(e,t))}}static createProperty(t,e=X){if(this._ensureClassProperties(),this._classProperties.set(t,e),e.noAccessor||this.prototype.hasOwnProperty(t))return;const i="symbol"==typeof t?Symbol():`__${t}`;Object.defineProperty(this.prototype,t,{get(){return this[i]},set(e){const r=this[t];this[i]=e,this._requestUpdate(t,r)},configurable:!0,enumerable:!0})}static finalize(){const t=Object.getPrototypeOf(this);if(t.hasOwnProperty(et)||t.finalize(),this[et]=!0,this._ensureClassProperties(),this._attributeToPropertyMap=new Map,this.hasOwnProperty(JSCompiler_renameProperty("properties",this))){const t=this.properties,e=[...Object.getOwnPropertyNames(t),..."function"==typeof Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(t):[]];for(const i of e)this.createProperty(i,t[i])}}static _attributeNameForProperty(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}static _valueHasChanged(t,e,i=G){return i(t,e)}static _propertyValueFromAttribute(t,e){const i=e.type,r=e.converter||F,s="function"==typeof r?r:r.fromAttribute;return s?s(t,i):t}static _propertyValueToAttribute(t,e){if(void 0===e.reflect)return;const i=e.type,r=e.converter;return(r&&r.toAttribute||F.toAttribute)(t,i)}initialize(){this._saveInstanceProperties(),this._requestUpdate()}_saveInstanceProperties(){this.constructor._classProperties.forEach((t,e)=>{if(this.hasOwnProperty(e)){const t=this[e];delete this[e],this._instanceProperties||(this._instanceProperties=new Map),this._instanceProperties.set(e,t)}})}_applyInstanceProperties(){this._instanceProperties.forEach((t,e)=>this[e]=t),this._instanceProperties=void 0}connectedCallback(){this._updateState=this._updateState|tt,this._hasConnectedResolver&&(this._hasConnectedResolver(),this._hasConnectedResolver=void 0)}disconnectedCallback(){}attributeChangedCallback(t,e,i){e!==i&&this._attributeToProperty(t,i)}_propertyToAttribute(t,e,i=X){const r=this.constructor,s=r._attributeNameForProperty(t,i);if(void 0!==s){const t=r._propertyValueToAttribute(e,i);if(void 0===t)return;this._updateState=this._updateState|K,null==t?this.removeAttribute(s):this.setAttribute(s,t),this._updateState=this._updateState&~K}}_attributeToProperty(t,e){if(this._updateState&K)return;const i=this.constructor,r=i._attributeToPropertyMap.get(t);if(void 0!==r){const t=i._classProperties.get(r)||X;this._updateState=this._updateState|Q,this[r]=i._propertyValueFromAttribute(e,t),this._updateState=this._updateState&~Q}}_requestUpdate(t,e){let i=!0;if(void 0!==t){const r=this.constructor,s=r._classProperties.get(t)||X;r._valueHasChanged(this[t],e,s.hasChanged)?(this._changedProperties.has(t)||this._changedProperties.set(t,e),!0!==s.reflect||this._updateState&Q||(void 0===this._reflectingProperties&&(this._reflectingProperties=new Map),this._reflectingProperties.set(t,s))):i=!1}!this._hasRequestedUpdate&&i&&this._enqueueUpdate()}requestUpdate(t,e){return this._requestUpdate(t,e),this.updateComplete}async _enqueueUpdate(){let t,e;this._updateState=this._updateState|Y;const i=this._updatePromise;this._updatePromise=new Promise((i,r)=>{t=i,e=r});try{await i}catch(r){}this._hasConnected||await new Promise(t=>this._hasConnectedResolver=t);try{const t=this.performUpdate();null!=t&&await t}catch(r){e(r)}t(!this._hasRequestedUpdate)}get _hasConnected(){return this._updateState&tt}get _hasRequestedUpdate(){return this._updateState&Y}get hasUpdated(){return this._updateState&Z}performUpdate(){this._instanceProperties&&this._applyInstanceProperties();let t=!1;const e=this._changedProperties;try{(t=this.shouldUpdate(e))&&this.update(e)}catch(i){throw t=!1,i}finally{this._markUpdated()}t&&(this._updateState&Z||(this._updateState=this._updateState|Z,this.firstUpdated(e)),this.updated(e))}_markUpdated(){this._changedProperties=new Map,this._updateState=this._updateState&~Y}get updateComplete(){return this._getUpdateComplete()}_getUpdateComplete(){return this._updatePromise}shouldUpdate(t){return!0}update(t){void 0!==this._reflectingProperties&&this._reflectingProperties.size>0&&(this._reflectingProperties.forEach((t,e)=>this._propertyToAttribute(e,this[e],t)),this._reflectingProperties=void 0)}updated(t){}firstUpdated(t){}}it[et]=!0;const rt="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,st=Symbol();class ot{constructor(t,e){if(e!==st)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t}get styleSheet(){return void 0===this._styleSheet&&(rt?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}const nt=(t,...e)=>{const i=e.reduce((e,i,r)=>e+(t=>{if(t instanceof ot)return t.cssText;if("number"==typeof t)return t;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${t}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(i)+t[r+1],t[0]);return new ot(i,st)};(window.litElementVersions||(window.litElementVersions=[])).push("2.2.1");const at=t=>t.flat?t.flat(1/0):function t(e,i=[]){for(let r=0,s=e.length;r<s;r++){const s=e[r];Array.isArray(s)?t(s,i):i.push(s)}return i}(t);class ct extends it{static finalize(){super.finalize.call(this),this._styles=this.hasOwnProperty(JSCompiler_renameProperty("styles",this))?this._getUniqueStyles():this._styles||[]}static _getUniqueStyles(){const t=this.styles,e=[];if(Array.isArray(t)){at(t).reduceRight((t,e)=>(t.add(e),t),new Set).forEach(t=>e.unshift(t))}else t&&e.push(t);return e}initialize(){super.initialize(),this.renderRoot=this.createRenderRoot(),window.ShadowRoot&&this.renderRoot instanceof window.ShadowRoot&&this.adoptStyles()}createRenderRoot(){return this.attachShadow({mode:"open"})}adoptStyles(){const t=this.constructor._styles;0!==t.length&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow?rt?this.renderRoot.adoptedStyleSheets=t.map(t=>t.styleSheet):this._needsShimAdoptedStyleSheets=!0:window.ShadyCSS.ScopingShim.prepareAdoptedCssText(t.map(t=>t.cssText),this.localName))}connectedCallback(){super.connectedCallback(),this.hasUpdated&&void 0!==window.ShadyCSS&&window.ShadyCSS.styleElement(this)}update(t){super.update(t);const e=this.render();e instanceof y&&this.constructor.render(e,this.renderRoot,{scopeName:this.localName,eventContext:this}),this._needsShimAdoptedStyleSheets&&(this._needsShimAdoptedStyleSheets=!1,this.constructor._styles.forEach(t=>{const e=document.createElement("style");e.textContent=t.cssText,this.renderRoot.appendChild(e)}))}render(){}}ct.finalized=!0,ct.render=((t,e,i)=>{if(!i||"object"!=typeof i||!i.scopeName)throw new Error("The `scopeName` option is required.");const r=i.scopeName,s=V.has(e),n=I&&11===e.nodeType&&!!e.host,a=n&&!q.has(r),c=a?document.createDocumentFragment():e;if(((t,e,i)=>{let r=V.get(e);void 0===r&&(o(e,e.firstChild),V.set(e,r=new S(Object.assign({templateFactory:N},i))),r.appendInto(e)),r.setValue(t),r.commit()})(t,c,Object.assign({templateFactory:W(r)},i)),a){const t=V.get(c);V.delete(c);const i=t.value instanceof _?t.value.template:void 0;H(r,c,i),o(e,e.firstChild),e.appendChild(c),V.set(e,t)}!s&&n&&window.ShadyCSS.styleElement(e.host)});const lt=new WeakMap,pt=i(t=>e=>{if(!(e instanceof k)||e instanceof E||"class"!==e.committer.name||e.committer.parts.length>1)throw new Error("The `classMap` directive must be used in the `class` attribute and must be the only part in the attribute.");const{committer:i}=e,{element:r}=i;lt.has(e)||(r.className=i.strings.join(" "));const{classList:s}=r,o=lt.get(e);for(const n in o)n in t||s.remove(n);for(const n in t){const e=t[n];if(!o||e!==o[n]){s[e?"add":"remove"](n)}}lt.set(e,t)}),ht=new WeakMap,dt=i(t=>e=>{if(!(e instanceof k)||e instanceof E||"style"!==e.committer.name||e.committer.parts.length>1)throw new Error("The `styleMap` directive must be used in the style attribute and must be the only part in the attribute.");const{committer:i}=e,{style:r}=i.element;ht.has(e)||(r.cssText=i.strings.join(" "));const s=ht.get(e);for(const o in s)o in t||(-1===o.indexOf("-")?r[o]=null:r.removeProperty(o));for(const o in t)-1===o.indexOf("-")?r[o]=t[o]:r.setProperty(o,t[o]);ht.set(e,t)});var ut=function(){if("undefined"!=typeof Map)return Map;function t(t,e){var i=-1;return t.some(function(t,r){return t[0]===e&&(i=r,!0)}),i}return function(){function e(){this.__entries__=[]}return Object.defineProperty(e.prototype,"size",{get:function(){return this.__entries__.length},enumerable:!0,configurable:!0}),e.prototype.get=function(e){var i=t(this.__entries__,e),r=this.__entries__[i];return r&&r[1]},e.prototype.set=function(e,i){var r=t(this.__entries__,e);~r?this.__entries__[r][1]=i:this.__entries__.push([e,i])},e.prototype.delete=function(e){var i=this.__entries__,r=t(i,e);~r&&i.splice(r,1)},e.prototype.has=function(e){return!!~t(this.__entries__,e)},e.prototype.clear=function(){this.__entries__.splice(0)},e.prototype.forEach=function(t,e){void 0===e&&(e=null);for(var i=0,r=this.__entries__;i<r.length;i++){var s=r[i];t.call(e,s[1],s[0])}},e}()}(),mt="undefined"!=typeof window&&"undefined"!=typeof document&&window.document===document,gt=void 0!==t&&t.Math===Math?t:"undefined"!=typeof self&&self.Math===Math?self:"undefined"!=typeof window&&window.Math===Math?window:Function("return this")(),ft="function"==typeof requestAnimationFrame?requestAnimationFrame.bind(gt):function(t){return setTimeout(function(){return t(Date.now())},1e3/60)},_t=2,vt=20,yt=["top","right","bottom","left","width","height","size","weight"],bt="undefined"!=typeof MutationObserver,wt=function(){function t(){this.connected_=!1,this.mutationEventsAdded_=!1,this.mutationsObserver_=null,this.observers_=[],this.onTransitionEnd_=this.onTransitionEnd_.bind(this),this.refresh=function(t,e){var i=!1,r=!1,s=0;function o(){i&&(i=!1,t()),r&&a()}function n(){ft(o)}function a(){var t=Date.now();if(i){if(t-s<_t)return;r=!0}else i=!0,r=!1,setTimeout(n,e);s=t}return a}(this.refresh.bind(this),vt)}return t.prototype.addObserver=function(t){~this.observers_.indexOf(t)||this.observers_.push(t),this.connected_||this.connect_()},t.prototype.removeObserver=function(t){var e=this.observers_,i=e.indexOf(t);~i&&e.splice(i,1),!e.length&&this.connected_&&this.disconnect_()},t.prototype.refresh=function(){this.updateObservers_()&&this.refresh()},t.prototype.updateObservers_=function(){var t=this.observers_.filter(function(t){return t.gatherActive(),t.hasActive()});return t.forEach(function(t){return t.broadcastActive()}),t.length>0},t.prototype.connect_=function(){mt&&!this.connected_&&(document.addEventListener("transitionend",this.onTransitionEnd_),window.addEventListener("resize",this.refresh),bt?(this.mutationsObserver_=new MutationObserver(this.refresh),this.mutationsObserver_.observe(document,{attributes:!0,childList:!0,characterData:!0,subtree:!0})):(document.addEventListener("DOMSubtreeModified",this.refresh),this.mutationEventsAdded_=!0),this.connected_=!0)},t.prototype.disconnect_=function(){mt&&this.connected_&&(document.removeEventListener("transitionend",this.onTransitionEnd_),window.removeEventListener("resize",this.refresh),this.mutationsObserver_&&this.mutationsObserver_.disconnect(),this.mutationEventsAdded_&&document.removeEventListener("DOMSubtreeModified",this.refresh),this.mutationsObserver_=null,this.mutationEventsAdded_=!1,this.connected_=!1)},t.prototype.onTransitionEnd_=function(t){var e=t.propertyName,i=void 0===e?"":e;yt.some(function(t){return!!~i.indexOf(t)})&&this.refresh()},t.getInstance=function(){return this.instance_||(this.instance_=new t),this.instance_},t.instance_=null,t}(),xt=function(t,e){for(var i=0,r=Object.keys(e);i<r.length;i++){var s=r[i];Object.defineProperty(t,s,{value:e[s],enumerable:!1,writable:!1,configurable:!0})}return t},kt=function(t){return t&&t.ownerDocument&&t.ownerDocument.defaultView||gt},St=At(0,0,0,0);function $t(t){return parseFloat(t)||0}function Pt(t){for(var e=[],i=1;i<arguments.length;i++)e[i-1]=arguments[i];return e.reduce(function(e,i){return e+$t(t["border-"+i+"-width"])},0)}function Et(t){var e=t.clientWidth,i=t.clientHeight;if(!e&&!i)return St;var r=kt(t).getComputedStyle(t),s=function(t){for(var e={},i=0,r=["top","right","bottom","left"];i<r.length;i++){var s=r[i],o=t["padding-"+s];e[s]=$t(o)}return e}(r),o=s.left+s.right,n=s.top+s.bottom,a=$t(r.width),c=$t(r.height);if("border-box"===r.boxSizing&&(Math.round(a+o)!==e&&(a-=Pt(r,"left","right")+o),Math.round(c+n)!==i&&(c-=Pt(r,"top","bottom")+n)),!function(t){return t===kt(t).document.documentElement}(t)){var l=Math.round(a+o)-e,p=Math.round(c+n)-i;1!==Math.abs(l)&&(a-=l),1!==Math.abs(p)&&(c-=p)}return At(s.left,s.top,a,c)}var Ct="undefined"!=typeof SVGGraphicsElement?function(t){return t instanceof kt(t).SVGGraphicsElement}:function(t){return t instanceof kt(t).SVGElement&&"function"==typeof t.getBBox};function Ot(t){return mt?Ct(t)?function(t){var e=t.getBBox();return At(0,0,e.width,e.height)}(t):Et(t):St}function At(t,e,i,r){return{x:t,y:e,width:i,height:r}}var Tt=function(){function t(t){this.broadcastWidth=0,this.broadcastHeight=0,this.contentRect_=At(0,0,0,0),this.target=t}return t.prototype.isActive=function(){var t=Ot(this.target);return this.contentRect_=t,t.width!==this.broadcastWidth||t.height!==this.broadcastHeight},t.prototype.broadcastRect=function(){var t=this.contentRect_;return this.broadcastWidth=t.width,this.broadcastHeight=t.height,t},t}(),Nt=function(){return function(t,e){var i,r,s,o,n,a,c,l=(r=(i=e).x,s=i.y,o=i.width,n=i.height,a="undefined"!=typeof DOMRectReadOnly?DOMRectReadOnly:Object,c=Object.create(a.prototype),xt(c,{x:r,y:s,width:o,height:n,top:s,right:r+o,bottom:n+s,left:r}),c);xt(this,{target:t,contentRect:l})}}(),Mt=function(){function t(t,e,i){if(this.activeObservations_=[],this.observations_=new ut,"function"!=typeof t)throw new TypeError("The callback provided as parameter 1 is not a function.");this.callback_=t,this.controller_=e,this.callbackCtx_=i}return t.prototype.observe=function(t){if(!arguments.length)throw new TypeError("1 argument required, but only 0 present.");if("undefined"!=typeof Element&&Element instanceof Object){if(!(t instanceof kt(t).Element))throw new TypeError('parameter 1 is not of type "Element".');var e=this.observations_;e.has(t)||(e.set(t,new Tt(t)),this.controller_.addObserver(this),this.controller_.refresh())}},t.prototype.unobserve=function(t){if(!arguments.length)throw new TypeError("1 argument required, but only 0 present.");if("undefined"!=typeof Element&&Element instanceof Object){if(!(t instanceof kt(t).Element))throw new TypeError('parameter 1 is not of type "Element".');var e=this.observations_;e.has(t)&&(e.delete(t),e.size||this.controller_.removeObserver(this))}},t.prototype.disconnect=function(){this.clearActive(),this.observations_.clear(),this.controller_.removeObserver(this)},t.prototype.gatherActive=function(){var t=this;this.clearActive(),this.observations_.forEach(function(e){e.isActive()&&t.activeObservations_.push(e)})},t.prototype.broadcastActive=function(){if(this.hasActive()){var t=this.callbackCtx_,e=this.activeObservations_.map(function(t){return new Nt(t.target,t.broadcastRect())});this.callback_.call(t,e,t),this.clearActive()}},t.prototype.clearActive=function(){this.activeObservations_.splice(0)},t.prototype.hasActive=function(){return this.activeObservations_.length>0},t}(),Vt="undefined"!=typeof WeakMap?new WeakMap:new ut,zt=function(){return function t(e){if(!(this instanceof t))throw new TypeError("Cannot call a class as a function.");if(!arguments.length)throw new TypeError("1 argument required, but only 0 present.");var i=wt.getInstance(),r=new Mt(e,i,this);Vt.set(this,r)}}();["observe","unobserve","disconnect"].forEach(function(t){zt.prototype[t]=function(){var e;return(e=Vt.get(this))[t].apply(e,arguments)}});var Rt=void 0!==gt.ResizeObserver?gt.ResizeObserver:zt;const jt={shuffle:!0,power_state:!0,artwork_border:!0,icon_state:!0,sound_mode:!0,runtime:!0,volume:!1,controls:!1,play_pause:!1,play_stop:!0},Lt={DEFAULT:"mdi:cast",DROPDOWN:"mdi:chevron-down",GROUP:"mdi:speaker-multiple",MENU:"mdi:menu-down",MUTE:{true:"mdi:volume-off",false:"mdi:volume-high"},NEXT:"mdi:skip-next",PLAY:{true:"mdi:pause",false:"mdi:play"},POWER:"mdi:power",PREV:"mdi:skip-previous",SEND:"mdi:send",SHUFFLE:"mdi:shuffle",STOP:{true:"mdi:stop",false:"mdi:play"},VOL_DOWN:"mdi:volume-minus",VOL_UP:"mdi:volume-plus"},Bt=["entity","_overflow","break","thumbnail","edit","idle"],Ut=["media_duration","media_position","media_position_updated_at"],It=390,Wt="Przekieruj media na",Dt=[{attr:"media_title"},{attr:"media_artist"},{attr:"media_series_title"},{attr:"media_season",prefix:"S"},{attr:"media_episode",prefix:"E"},{attr:"app_name"}];class qt{constructor(t,e,i){this.hass=t||{},this.config=e||{},this.entity=i||{},this.state=i.state,this.attr=i.attributes,this.idle=!!e.idle_view&&this.idleView,this.active=this.isActive}get id(){return this.entity.entity_id}get icon(){return this.attr.icon}get isPaused(){return"paused"===this.state}get isPlaying(){return"playing"===this.state}get isIdle(){return"idle"===this.state}get isStandby(){return"standby"===this.state}get isUnavailable(){return"unavailable"===this.state}get isOff(){return"off"===this.state}get isActive(){return!this.isOff&&!this.isUnavailable&&!this.idle||!1}get shuffle(){return this.attr.shuffle||!1}get content(){return this.attr.media_content_type||"none"}get mediaDuration(){return this.attr.media_duration||0}get updatedAt(){return this.attr.media_position_updated_at||0}get position(){return this.attr.media_position||0}get name(){return this.attr.friendly_name||""}get groupCount(){return this.group.length}get isGrouped(){return this.group.length>1}get group(){const t=`${this.config.speaker_group.platform}_group`;return this.attr[t]||[]}get master(){return this.config.entity}get isMaster(){return this.master===this.config.entity}get sources(){return this.attr.source_list||[]}get source(){return this.attr.source||""}get soundModes(){return this.attr.sound_mode_list||[]}get soundMode(){return this.attr.sound_mode||""}get muted(){return this.attr.is_volume_muted||!1}get vol(){return this.attr.volume_level||0}get picture(){return this.attr.entity_picture_local||this.attr.entity_picture}get hasArtwork(){return this.picture&&"none"!==this.config.artwork&&this.active&&!this.idle}get mediaInfo(){return Dt.map(t=>Object.assign({text:this.attr[t.attr],prefix:""},t)).filter(t=>t.text)}get hasProgress(){return!this.config.hide.progress&&!this.idle&&Ut.every(t=>t in this.attr)}get progress(){return this.position+(Date.now()-new Date(this.updatedAt).getTime())/1e3}get idleView(){const t=this.config.idle_view;return!!(t.when_idle&&this.isIdle||t.when_standby&&this.isStandby||t.when_paused&&this.isPaused)||!(!this.updatedAt||!t.after||this.isPlaying)&&this.checkIdleAfter(t.after)}get trackIdle(){return this.active&&!this.isPlaying&&this.updatedAt&&this.config.idle_view&&this.config.idle_view.after}checkIdleAfter(t){const e=(Date.now()-new Date(this.updatedAt).getTime())/1e3;return this.idle=e>60*t,this.active=this.isActive,this.idle}get supportsShuffle(){return!(void 0===this.attr.shuffle)}get supportsMute(){return!(void 0===this.attr.is_volume_muted)}getAttribute(t){return this.attr[t]||""}get artwork(){return`url(${this.attr.entity_picture_local?this.hass.hassUrl(this.picture):this.picture})`}toggle(t){return this.config.toggle_power?this.callService(t,"toggle"):this.isOff?this.callService(t,"turn_on"):void this.callService(t,"turn_off")}toggleMute(t){this.callService(t,"volume_mute",{is_volume_muted:!this.muted})}toggleShuffle(t){this.callService(t,"shuffle_set",{shuffle:!this.shuffle})}setSource(t,e){this.callService(t,"select_source",{source:e})}setMedia(t,e){this.callService(t,"play_media",Object.assign({},e))}playPause(t){this.callService(t,"media_play_pause")}playStop(t){this.isPlaying?this.callService(t,"media_stop"):this.callService(t,"media_play")}setSoundMode(t,e){this.callService(t,"select_sound_mode",{sound_mode:e})}next(t){this.callService(t,"media_next_track")}prev(t){this.callService(t,"media_previous_track")}stop(t){this.callService(t,"media_stop")}volumeUp(t){this.callService(t,"volume_up")}volumeDown(t){this.callService(t,"volume_down")}seek(t,e){this.callService(t,"media_seek",{seek_position:e})}setVolume(t,e){this.config.speaker_group.sync_volume?this.group.forEach(i=>{const r=this.config.speaker_group.entities.find(t=>t.entity_id===i)||{};let s=e;r.volume_offset&&((s+=r.volume_offset/100)>1&&(s=1),s<0&&(s=0)),this.callService(t,"volume_set",{entity_id:i,volume_level:s})}):this.callService(t,"volume_set",{entity_id:this.config.entity,volume_level:e})}handleGroupChange(t,e,i){const{platform:r}=this.config.speaker_group,s={entity_id:e};if(i){if(s.master=this.config.entity,"bluesound"===r)return this.callService(t,`${r}_JOIN`,s);this.callService(t,"join",s,r)}else{if("bluesound"===r)return this.callService(t,`${r}_UNJOIN`,s);this.callService(t,"unjoin",s,r)}}toggleScript(t,e,i={}){this.callService(t,e.split(".").pop(),Object.assign({},i),"script")}toggleService(t,e,i={}){t.stopPropagation();const[r,s]=e.split(".");this.hass.callService(r,s,Object.assign({},i))}callService(t,e,i,r="media_player"){t.stopPropagation(),this.hass.callService(r,e,Object.assign({entity_id:this.config.entity},i))}}const Ht=nt`
    :host {
      overflow: visible !important;
      display: block;
      --mmp-scale: var(--mini-media-player-scale, 1);
      --mmp-unit: calc(var(--mmp-scale) * 40px);
      --mmp-accent-color: var(
        --mini-media-player-accent-color,
        var(--accent-color, #f39c12)
      );
      --mmp-base-color: var(
        --mini-media-player-base-color,
        var(--primary-text-color, #000)
      );
      --mmp-overlay-color: var(
        --mini-media-player-overlay-color,
        rgba(0, 0, 0, 0.5)
      );
      --mmp-overlay-color-stop: var(
        --mini-media-player-overlay-color-stop,
        25%
      );
      --mmp-overlay-base-color: var(
        --mini-media-player-overlay-base-color,
        #fff
      );
      --mmp-overlay-accent-color: var(
        --mini-media-player-overlay-accent-color,
        --mmp-accent-color
      );
      --mmp-text-color: var(
        --mini-media-player-base-color,
        var(--primary-text-color, #000)
      );
      --mmp-media-cover-info-color: var(
        --mini-media-player-media-cover-info-color,
        --mmp-text-color
      );
      --mmp-text-color-inverted: var(--disabled-text-color);
      --mmp-active-color: var(--mmp-accent-color);
      --mmp-icon-color: var(
        --mini-media-player-icon-color,
        var(
          --mini-media-player-base-color,
          var(--paper-item-icon-color, #44739e)
        )
      );
      --mmp-icon-active-color: var(
        --paper-item-icon-active-color,
        --mmp-active-color
      );
      --mmp-info-opacity: 1;
      --mmp-bg-opacity: var(--mini-media-player-background-opacity, 1);
      --mmp-artwork-opacity: var(--mini-media-player-artwork-opacity, 1);
      --mmp-progress-height: var(--mini-media-player-progress-height, 6px);
      --mdc-theme-primary: var(--mmp-text-color);
      --mdc-theme-on-primary: var(--mmp-text-color);
      --paper-checkbox-unchecked-color: var(--mmp-text-color);
      --paper-checkbox-label-color: var(--mmp-text-color);
      color: var(--mmp-text-color);
    }
    ha-card.--bg {
      --mmp-info-opacity: 0.75;
    }
    ha-card.--has-artwork[artwork*="cover"] {
      --mmp-accent-color: var(
        --mini-media-player-overlay-accent-color,
        var(--mini-media-player-accent-color, var(--accent-color, #f39c12))
      );
      --mmp-text-color: var(--mmp-overlay-base-color);
      --mmp-text-color-inverted: #000;
      --mmp-active-color: rgba(255, 255, 255, 0.5);
      --mmp-icon-color: var(--mmp-text-color);
      --mmp-icon-active-color: var(--mmp-text-color);
      --mmp-info-opacity: 0.75;
      --paper-slider-container-color: var(
        --mini-media-player-overlay-color,
        rgba(255, 255, 255, 0.75)
      );
      --mdc-theme-primary: var(--mmp-text-color);
      --mdc-theme-on-primary: var(--mmp-text-color);
      --paper-checkbox-unchecked-color: var(--mmp-text-color);
      --paper-checkbox-label-color: var(--mmp-text-color);
      color: var(--mmp-text-color);
    }
    ha-card {
      cursor: default;
      display: flex;
      background: transparent;
      overflow: visible;
      padding: 0;
      position: relative;
      color: inherit;
      font-size: calc(var(--mmp-unit) * 0.35);
    }
    ha-card.--group {
      box-shadow: none;
      --mmp-progress-height: var(--mini-media-player-progress-height, 4px);
    }
    ha-card.--more-info {
      cursor: pointer;
    }
    .mmp__bg,
    .mmp-player,
    .mmp__container {
      border-radius: var(--ha-card-border-radius, 0);
    }
    .mmp__container {
      overflow: hidden;
      height: 100%;
      width: 100%;
      position: absolute;
      pointer-events: none;
    }
    ha-card:before {
      content: "";
      padding-top: 0px;
      transition: padding-top 0.5s cubic-bezier(0.21, 0.61, 0.35, 1);
      will-change: padding-top;
    }
    ha-card.--initial .entity__artwork,
    ha-card.--initial .entity__icon {
      animation-duration: 0.001s;
    }
    ha-card.--initial:before,
    ha-card.--initial .mmp-player {
      transition: none;
    }
    header {
      display: none;
    }
    ha-card[artwork="full-cover"].--has-artwork:before {
      padding-top: 56%;
    }
    ha-card[artwork="full-cover"].--has-artwork[content="music"]:before,
    ha-card[artwork="full-cover-fit"].--has-artwork:before {
      padding-top: 100%;
    }
    .mmp__bg {
      background: var(
        --ha-card-background,
        var(--paper-card-background-color, white)
      );
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      overflow: hidden;
      -webkit-transform: translateZ(0);
      transform: translateZ(0);
      opacity: var(--mmp-bg-opacity);
    }
    ha-card[artwork*="cover"].--has-artwork .mmp__bg {
      opacity: var(--mmp-artwork-opacity);
      background: transparent;
    }
    ha-card.--group .mmp__bg {
      background: transparent;
    }
    .cover,
    .cover:before {
      display: block;
      opacity: 0;
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      transition: opacity 0.75s cubic-bezier(0.21, 0.61, 0.35, 1);
      will-change: opacity;
    }
    .cover {
      animation: fade-in 0.5s cubic-bezier(0.21, 0.61, 0.35, 1);
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center center;
      border-radius: var(--ha-card-border-radius, 0);
      overflow: hidden;
    }
    .cover:before {
      background: var(--mmp-overlay-color);
      content: "";
    }
    ha-card[artwork*="full-cover"].--has-artwork .mmp-player {
      background: linear-gradient(
        to top,
        var(--mmp-overlay-color) var(--mmp-overlay-color-stop),
        transparent 100%
      );
      border-bottom-left-radius: var(--ha-card-border-radius, 0);
      border-bottom-right-radius: var(--ha-card-border-radius, 0);
    }
    ha-card.--has-artwork .cover,
    ha-card.--has-artwork[artwork="cover"] .cover:before,
    ha-card.--bg .cover {
      opacity: 0.999;
    }
    ha-card[artwork="default"] .cover {
      display: none;
    }
    ha-card.--bg .cover {
      display: block;
    }
    ha-card[artwork="full-cover-fit"].--has-artwork .cover {
      background-color: black;
      background-size: contain;
    }
    .mmp-player {
      align-self: flex-end;
      box-sizing: border-box;
      position: relative;
      padding: 16px;
      transition: padding 0.25s ease-out;
      width: 100%;
      will-change: padding;
    }
    ha-card.--group .mmp-player {
      padding: 2px 0;
    }
    .flex {
      display: flex;
      display: -ms-flexbox;
      display: -webkit-flex;
      flex-direction: row;
    }
    .mmp-player__core {
      position: relative;
    }
    .entity__info {
      justify-content: center;
      display: flex;
      flex-direction: column;
      margin-left: 8px;
      position: relative;
      overflow: hidden;
      user-select: none;
    }
    ha-card.--rtl .entity__info {
      margin-left: auto;
      margin-right: calc(var(--mmp-unit) / 5);
    }
    ha-card[content="movie"] .attr__media_season,
    ha-card[content="movie"] .attr__media_episode {
      display: none;
    }
    .entity__icon {
      color: var(--mmp-icon-color);
    }
    .entity__icon[color] {
      color: var(--mmp-icon-active-color);
    }
    .entity__artwork,
    .entity__icon {
      animation: fade-in 0.25s ease-out;
      background-position: center center;
      background-repeat: no-repeat;
      background-size: cover;
      border-radius: 100%;
      height: var(--mmp-unit);
      width: var(--mmp-unit);
      min-width: var(--mmp-unit);
      line-height: var(--mmp-unit);
      margin-right: calc(var(--mmp-unit) / 5);
      position: relative;
      text-align: center;
      will-change: border-color;
      transition: border-color 0.25s ease-out;
    }
    ha-card.--rtl .entity__artwork,
    ha-card.--rtl .entity__icon {
      margin-right: auto;
    }
    .entity__artwork[border] {
      border: 2px solid var(--primary-text-color);
      box-sizing: border-box;
      -moz-box-sizing: border-box;
      -webkit-box-sizing: border-box;
    }
    .entity__artwork[border][state="playing"] {
      border-color: var(--mmp-accent-color);
    }
    .entity__info__name,
    .entity__info__media[short] {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .entity__info__name {
      line-height: calc(var(--mmp-unit) / 2);
      color: var(--mmp-text-color);
    }
    .entity__info__media {
      color: var(--secondary-text-color);
      max-height: 6em;
      word-break: break-word;
      opacity: var(--mmp-info-opacity);
      transition: color 0.5s;
    }
    .entity__info__media[short] {
      max-height: calc(var(--mmp-unit) / 2);
      overflow: hidden;
    }
    .attr__app_name {
      display: none;
    }
    .attr__app_name:first-child,
    .attr__app_name:first-of-type {
      display: inline;
    }
    .mmp-player__core[inactive] .entity__info__media {
      color: var(--mmp-text-color);
      max-width: 200px;
      opacity: 0.5;
    }
    .entity__info__media[short-scroll] {
      max-height: calc(var(--mmp-unit) / 2);
      white-space: nowrap;
    }
    .entity__info__media[scroll] > span {
      visibility: hidden;
    }
    .entity__info__media[scroll] > div {
      animation: move linear infinite;
    }
    .entity__info__media[scroll] .marquee {
      animation: slide linear infinite;
    }
    .entity__info__media[scroll] .marquee,
    .entity__info__media[scroll] > div {
      animation-duration: inherit;
      visibility: visible;
    }
    .entity__info__media[scroll] {
      animation-duration: 10s;
      mask-image: linear-gradient(
        to right,
        transparent 0%,
        black 5%,
        black 95%,
        transparent 100%
      );
      -webkit-mask-image: linear-gradient(
        to right,
        transparent 0%,
        black 5%,
        black 95%,
        transparent 100%
      );
    }
    .marquee {
      visibility: hidden;
      position: absolute;
      white-space: nowrap;
    }
    ha-card[artwork*="cover"].--has-artwork .entity__info__media,
    ha-card.--bg .entity__info__media {
      color: var(--mmp-media-cover-info-color);
    }
    .entity__info__media span:before {
      content: " - ";
    }
    .entity__info__media span:first-of-type:before {
      content: "";
    }
    .entity__info__media span:empty {
      display: none;
    }
    .mmp-player__adds {
      margin-left: calc(var(--mmp-unit) * 1.2);
      position: relative;
    }
    ha-card.--rtl .mmp-player__adds {
      margin-left: auto;
      margin-right: calc(var(--mmp-unit) * 1.2);
    }
    .mmp-player__adds > *:nth-child(2) {
      margin-top: 0px;
    }
    mmp-powerstrip {
      flex: 1;
      justify-content: flex-end;
      margin-right: 0;
      margin-left: auto;
      width: auto;
      max-width: 100%;
    }
    mmp-media-controls {
      flex-wrap: wrap;
    }
    ha-card.--flow mmp-powerstrip {
      justify-content: space-between;
      margin-left: auto;
    }
    ha-card.--flow.--rtl mmp-powerstrip {
      margin-right: auto;
    }
    ha-card.--flow .entity__info {
      display: none;
    }
    ha-card.--responsive .mmp-player__adds {
      margin-left: 0;
    }
    ha-card.--responsive.--rtl .mmp-player__adds {
      margin-right: 0;
    }
    ha-card.--responsive .mmp-player__adds > mmp-media-controls {
      padding: 0;
    }
    ha-card.--progress .mmp-player {
      padding-bottom: calc(
        16px + calc(var(--mini-media-player-progress-height, 6px) - 6px)
      );
    }
    ha-card.--progress.--group .mmp-player {
      padding-bottom: calc(
        10px + calc(var(--mini-media-player-progress-height, 6px) - 6px)
      );
    }
    ha-card.--runtime .mmp-player {
      padding-bottom: calc(
        16px + 16px + var(--mini-media-player-progress-height, 0px)
      );
    }
    ha-card.--runtime.--group .mmp-player {
      padding-bottom: calc(
        16px + 12px + var(--mini-media-player-progress-height, 0px)
      );
    }
    ha-card.--inactive .mmp-player {
      padding: 16px;
    }
    ha-card.--inactive.--group .mmp-player {
      padding: 2px 0;
    }
    .mmp-player div:empty {
      display: none;
    }
    @keyframes slide {
      100% {
        transform: translateX(-100%);
      }
    }
    @keyframes move {
      from {
        transform: translateX(100%);
      }
      to {
        transform: translateX(0);
      }
    }
    @keyframes fade-in {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  `,Ft=nt`
    .ellipsis {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .label {
      margin: 0 8px;
    }
    ha-icon {
      width: calc(var(--mmp-unit) * 0.6);
      height: calc(var(--mmp-unit) * 0.6);
    }
    paper-icon-button {
      width: var(--mmp-unit);
      height: var(--mmp-unit);
      color: var(--mmp-text-color, var(--primary-text-color));
      transition: color 0.25s;
    }
    paper-icon-button[color] {
      color: var(--mmp-accent-color, var(--accent-color)) !important;
      opacity: 1 !important;
    }
    paper-icon-button[inactive] {
      opacity: 0.5;
    }
  `;var Gt=(t,e,i,r,s)=>{let o;switch(r.action){case"more-info":(o=new Event("hass-more-info",{composed:!0})).detail={entityId:r.entity||s},t.dispatchEvent(o);break;case"navigate":if(!r.navigation_path)return;window.history.pushState(null,"",r.navigation_path),(o=new Event("location-changed",{composed:!0})).detail={replace:!1},window.dispatchEvent(o);break;case"call-service":{if(!r.service)return;const[t,i]=r.service.split(".",2),s=Object.assign({},r.service_data);e.callService(t,i,s);break}case"url":if(!r.url)return;window.location.href=r.url}};customElements.define("mmp-group-item",class extends ct{static get properties(){return{item:{},checked:Boolean,disabled:Boolean,master:Boolean}}render(){return z`
        <paper-checkbox
          ?checked=${this.checked}
          ?disabled=${this.disabled}
          @change="${t=>t.stopPropagation()}"
          @click="${this.handleClick}"
        >
          ${this.item.name}
          ${this.master?z`
                <span>(master)</span>
              `:""}
        </paper-checkbox>
      `}handleClick(t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("change",{detail:{entity:this.item.entity_id,checked:!this.checked}}))}static get styles(){return nt`
        paper-checkbox {
          padding: 8px 0;
        }
        paper-checkbox > span {
          font-weight: 600;
        }

        ha-card[artwork*="cover"][has-artwork] paper-checkbox[disabled] {
          --paper-checkbox-checkmark-color: rgba(0, 0, 0, 0.5);
        }
        ha-card[artwork*="cover"][has-artwork] paper-checkbox {
          --paper-checkbox-unchecked-color: #ffffff;
          --paper-checkbox-label-color: #ffffff;
        }`}}),customElements.define("mmp-button",class extends ct{render(){return z`
        <div class="container">
          <div class="slot-container">
            <slot></slot>
          </div>
          <paper-ripple></paper-ripple>
        </div>
      `}static get styles(){return nt`
        :host {
          position: relative;
          box-sizing: border-box;
          margin: 4px;
          min-width: 0;
          overflow: hidden;
          transition: background 0.5s;
        }
        :host([raised]) {
          background: rgba(255, 255, 255, 0.25);
          min-height: calc(var(--mmp-unit) * 0.8);
          box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, 0.2),
            0px 2px 2px 0px rgba(0, 0, 0, 0.14),
            0px 1px 5px 0px rgba(0, 0, 0, 0.12);
        }
        :host([color]) {
          background: var(--mmp-active-color);
          transition: background 0.25s;
          opacity: 1;
        }
        :host([faded]) {
          opacity: 0.75;
        }
        .container {
          height: 100%;
          width: 100%;
        }
        .slot-container {
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 8px;
          width: auto;
        }
        paper-ripple {
          position: absolute;
          left: 0;
          right: 0;
          top: 0;
          bottom: 0;
        }`}}),customElements.define("mmp-group-list",class extends ct{static get properties(){return{entities:{},player:{},visible:Boolean}}get group(){return this.player.group}get master(){return this.player.master}get isMaster(){return this.player.isMaster}handleGroupChange(t){const{entity:e,checked:i}=t.detail;this.player.handleGroupChange(t,e,i)}render({group:t,master:e,isMaster:i}=this){return this.visible?z`
            <div class="mmp-group-list" ?visible=${this.visible}>
              <span class="mmp-group-list__title">GRUPA ODTWARZACZY</span>
              ${this.entities.map(i=>z`
                  <mmp-group-item
                    @change=${this.handleGroupChange}
                    .item=${i}
                    .checked=${i.entity_id===this.player.id||t.includes(i.entity_id)}
                    .disabled=${i.entity_id===this.player.id||e!==this.player.id}
                    .master=${i.entity_id===e}
                  />
                `)}
              <div class="mmp-group-list__buttons">
                <mmp-button
                  class="mmp-group-list__button"
                  raised
                  ?disabled=${t.length<2}
                  @click=${e=>this.player.handleGroupChange(e,i?t:this.player.entity_id,!1)}
                >
                  <span
                    >${i?z`
                          <svg
                            style="width:24px;height:24px; vertical-align:middle;"
                            viewBox="0 0 24 24"
                          >
                            <path
                              fill="#fff"
                              d="M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3M19,5V19H5V5H19Z"
                            />
                          </svg>
                          Wszystkie
                        `:z`
                          Opuść
                        `}</span
                  >
                </mmp-button>
                <mmp-button
                  class="mmp-group-list__button"
                  raised
                  ?disabled=${!i}
                  @click=${t=>this.player.handleGroupChange(t,this.entities.map(t=>t.entity_id),!0)}
                >
                  <span
                    ><svg
                      style="width:24px;height:24px; vertical-align:middle;"
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="#fff"
                        d="M19,19H5V5H15V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V11H19M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"
                      />
                    </svg>
                    Wszystkie</span
                  >
                </mmp-button>
              </div>
            </div>
          `:z``}static get styles(){return nt`
        .mmp-group-list {
          display: flex;
          flex-direction: column;
          margin-left: 8px;
          margin-bottom: 8px;
        }
        .mmp-group-list__title {
          font-weight: 500;
          letter-spacing: 0.1em;
          margin: 8px 0 4px;
          text-transform: uppercase;
        }
        .mmp-group-list__buttons {
          display: flex;
        }
        .mmp-group-list__button {
          margin: 8px 8px 0 0;
          min-width: 0;
          text-transform: uppercase;
          text-align: center;
          width: 50%;
          --mdc-theme-primary: transparent;
          background: rgba(255, 255, 255, 0.25);
        }`}}),customElements.define("mmp-dropdown",class extends ct{static get properties(){return{items:[],label:String,selected:String}}get selectedId(){return this.items.map(t=>t.id).indexOf(this.selected)}onChange(t){const e=t.target.selected;e!==this.selectedId&&this.items[e]&&(this.dispatchEvent(new CustomEvent("change",{detail:this.items[e]})),t.target.selected=-1)}render(){return z`
        <paper-menu-button
          class="mmp-dropdown"
          noink
          no-animations
          .horizontalAlign=${"right"}
          .verticalAlign=${"top"}
          .verticalOffset=${44}
          .dynamicAlign=${!0}
          @click=${t=>t.stopPropagation()}
        >
          ${this.icon?z`
                <paper-icon-button
                  class="mmp-dropdown__button icon"
                  slot="dropdown-trigger"
                  .icon=${Lt.DROPDOWN}
                >
                </paper-icon-button>
              `:z`
                <mmp-button
                  class="mmp-dropdown__button"
                  slot="dropdown-trigger"
                >
                  <div>
                    <span class="mmp-dropdown__label ellipsis">
                      ${this.selected||this.label}
                    </span>
                    <iron-icon
                      class="mmp-dropdown__icon"
                      .icon=${Lt.DROPDOWN}
                    ></iron-icon>
                  </div>
                </mmp-button>
              `}
          <paper-listbox
            slot="dropdown-content"
            .selected=${this.selectedId}
            @iron-select=${this.onChange}
          >
            ${this.items.map(t=>z`
                <paper-item value=${t.id||t.name}>
                  ${t.icon?z`
                        <iron-icon .icon=${t.icon}></iron-icon>
                      `:""}
                  ${t.name?z`
                        <span class="mmp-dropdown__item__label"
                          >${t.name}</span
                        >
                      `:""}
                </paper-item>
              `)}
          </paper-listbox>
        </paper-menu-button>
      `}static get styles(){return[Ft,nt`
          :host {
            display: block;
          }
          :host([faded]) {
            opacity: 0.75;
          }
          :host[small] .mmp-dropdown__label {
            max-width: 60px;
            display: block;
            position: relative;
            width: auto;
            text-transform: initial;
          }
          :host[full] .mmp-dropdown__label {
            max-width: none;
          }
          .mmp-dropdown {
            padding: 0;
            display: block;
          }
          .mmp-dropdown__button {
            display: flex;
            font-size: 1em;
            justify-content: space-between;
            align-items: center;
            height: calc(var(--mmp-unit) - 4px);
            margin: 2px 0;
          }
          .mmp-dropdown__button.icon {
            height: var(--mmp-unit);
            margin: 0;
          }
          .mmp-dropdown__button > div {
            display: flex;
            flex: 1;
            justify-content: space-between;
            align-items: center;
            height: calc(var(--mmp-unit) - 4px);
            max-width: 100%;
          }
          .mmp-dropdown__label {
            text-align: left;
            text-transform: none;
          }
          .mmp-dropdown__icon {
            height: calc(var(--mmp-unit) * 0.6);
            width: calc(var(--mmp-unit) * 0.6);
            min-width: calc(var(--mmp-unit) * 0.6);
          }
          paper-item > *:nth-child(2) {
            margin-left: 4px;
          }
          paper-menu-button[focused] mmp-button iron-icon {
            color: var(--mmp-accent-color);
            transform: rotate(180deg);
          }
          paper-menu-button[focused] paper-icon-button {
            color: var(--mmp-accent-color);
            transform: rotate(180deg);
          }
          paper-menu-button[focused] paper-icon-button[focused] {
            color: var(--mmp-text-color);
            transform: rotate(0deg);
          }
        `]}}),customElements.define("mmp-shortcuts",class extends ct{static get properties(){return{player:{},hass:{},shortcuts:{}}}get buttons(){return this.shortcuts.buttons}get list(){let t;this.shortcuts.list=[];const e=Object.keys(this.hass.states);for(t=0;t<e.length;t+=1)if(e[t].startsWith("media_player.")&&""!==this.hass.states[e[t]].entity_id){const i=this.hass.states[e[t]].attributes;this.shortcuts.list.push({name:i.friendly_name,icon:"mdi:speaker",id:"ais_exo_player.redirect_media",type:"service",data:{entity_id:this.hass.states[e[t]].entity_id}})}return this.shortcuts.list.push({name:"Wyszukaj dostępne odtwarzacze",icon:"mdi:sync",id:"ais_shell_command.scan_network_for_ais_players",type:"service"}),this.shortcuts.list}get show(){return!this.shortcuts.hide_when_off||this.player.active}get active(){return this.player.getAttribute(this.shortcuts.attribute)}get height(){return this.shortcuts.column_height||36}render(){if(!this.show)return z``;const{active:t}=this,e=this.list?z`
            <mmp-dropdown
              class="mmp-shortcuts__dropdown"
              @change=${this.handleShortcut}
              .items=${this.list}
              .label=${this.shortcuts.label}
              .selected=${t}
            >
            </mmp-dropdown>
          `:"",i=this.buttons?z`
            <div class="mmp-shortcuts__buttons">
              ${this.buttons.map(e=>z`
                  <mmp-button
                    style=${`min-height: ${this.height}px;`}
                    raised
                    columns=${this.shortcuts.columns}
                    ?color=${e.id===t}
                    class="mmp-shortcuts__button"
                    @click=${t=>this.handleShortcut(t,e)}
                  >
                    <div align=${this.shortcuts.align_text}>
                      ${e.icon?z`
                            <iron-icon .icon=${e.icon}></iron-icon>
                          `:""}
                      ${e.image?z`
                            <img src=${e.image} />
                          `:""}
                      ${e.name?z`
                            <span class="ellipsis">${e.name}</span>
                          `:""}
                    </div>
                  </mmp-button>
                `)}
            </div>
          `:"";return z`
        ${i} ${e}
      `}handleShortcut(t,e){const{type:i,id:r,data:s}=e||t.detail;if("source"===i)return this.player.setSource(t,r);if("service"===i)return this.player.toggleService(t,r,s);if("script"===i)return this.player.toggleScript(t,r,s);if("sound_mode"===i)return this.player.setSoundMode(t,r);const o={media_content_type:i,media_content_id:r};this.player.setMedia(t,o)}static get styles(){return[Ft,nt`
          .mmp-shortcuts__buttons {
            box-sizing: border-box;
            display: flex;
            flex-wrap: wrap;
            margin-top: 8px;
          }
          .mmp-shortcuts__button {
            min-width: calc(50% - 8px);
            flex: 1;
          }
          .mmp-shortcuts__button > div {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding: 0.2em 0;
          }
          .mmp-shortcuts__button > div[align="left"] {
            justify-content: flex-start;
          }
          .mmp-shortcuts__button > div[align="right"] {
            justify-content: flex-end;
          }
          .mmp-shortcuts__button[columns="1"] {
            min-width: calc(100% - 8px);
          }
          .mmp-shortcuts__button[columns="3"] {
            min-width: calc(33.33% - 8px);
          }
          .mmp-shortcuts__button[columns="4"] {
            min-width: calc(25% - 8px);
          }
          .mmp-shortcuts__button[columns="5"] {
            min-width: calc(20% - 8px);
          }
          .mmp-shortcuts__button[columns="6"] {
            min-width: calc(16.66% - 8px);
          }
          .mmp-shortcuts__button > div > span {
            line-height: calc(var(--mmp-unit) * 0.6);
            text-transform: initial;
          }
          .mmp-shortcuts__button > div > iron-icon {
            width: calc(var(--mmp-unit) * 0.6);
            height: calc(var(--mmp-unit) * 0.6);
          }
          .mmp-shortcuts__button > div > *:nth-child(2) {
            margin-left: 4px;
          }
          .mmp-shortcuts__button > div > img {
            height: 24px;
          }
        `]}}),customElements.define("mmp-tts",class extends ct{static get properties(){return{hass:{},config:{}}}get label(){return"Wyślij media lub tekst do odtwarzaczy"}get input(){return this.shadowRoot.getElementById("tts-input")}get message(){return this.input.value}render(){return z`
        <paper-input
          id="tts-input"
          class="mmp-tts__input"
          no-label-float
          placeholder="${this.label}..."
          @keypress=${this.handleTtsKeyPres}
          @click=${t=>t.stopPropagation()}
        >
        </paper-input>
        <paper-icon-button
          class="mmp-tts__button"
          icon="mdi:play-outline"
          @click=${this.handleTts}
        >
        </paper-icon-button>
      `}validURL(t){return!!new RegExp("^(https?:\\/\\/)?((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|((\\d{1,3}\\.){3}\\d{1,3}))(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*(\\?[;&a-z\\d%_.~+=-]*)?(\\#[-a-z\\d_]*)?$","i").test(t)}handleTtsKeyPres(t){if(13!==t.charCode)return t.stopPropagation(),!0;this.handleTts(t)}handleTts(t){const{config:e,message:i}=this,r={message:i,entity_id:e.entity_id||this.entity};e.language&&(r.language=e.language),"alexa"===e.platform?this.hass.callService("notify","alexa_media",{message:i,data:{type:e.type||"tts"},target:r.entity_id}):"sonos"===e.platform?this.hass.callService("script","sonos_say",{sonos_entity:r.entity_id,volume:e.volume||.5,message:i}):"webos"===e.platform?this.hass.callService("notify",r.entity_id.split(".").slice(-1)[0],{message:i}):"ga"===e.platform?this.hass.callService("notify","ga_broadcast",{message:i}):"ais"===e.platform?this.hass.callService("ais_exo_player","play_text_or_url",{text:i}):this.hass.callService("tts",`${e.platform}_say`,r),t.stopPropagation()}reset(){this.input.value=""}static get styles(){return nt`
        :host {
          align-items: center;
          margin-left: 8px;
          display: flex;
        }
        .mmp-tts__input {
          cursor: text;
          flex: 1;
          margin-right: 8px;
          --paper-input-container-input: {
            font-size: 1em;
          }
        }
        ha-card[rtl] .mmp-tts__input {
          margin-right: auto;
          margin-left: 8px;
        }
        .mmp-tts__button {
          margin: 0;
          height: 30px;
          padding: 0 0.4em;
        }
        paper-input {
          opacity: 0.75;
          --paper-input-container-color: var(--mmp-text-color);
          --paper-input-container-focus-color: var(--mmp-text-color);
          --paper-input-container: {
            padding: 0;
          }
        }
        paper-input[focused] {
          opacity: 1;
        }

        ha-card[artwork*="cover"][has-artwork] paper-input {
          --paper-input-container-focus-color: #ffffff;
        }
        ha-card[artwork*="cover"][has-artwork] paper-input {
          --paper-input-container-color: #ffffff;
          --paper-input-container-input-color: #ffffff;
        }`}});var Xt=t=>{let e=parseInt(t%60,10),i=parseInt(t/60%60,10),r=parseInt(t/3600%24,10);return i=i<10?`0${i}`:i,e=e<10?`0${e}`:e,"00"===(r=r<10?`0${r}`:r)&&"00"===i&&"00"===e?"":`${"00"!==r?`${r}:`:""}${i}:${e}`};customElements.define("mmp-progress",class extends ct{static get properties(){return{_player:{},showTime:Boolean,progress:Number,duration:Number,tracker:{},seekProgress:Number,seekWidth:Number,track:Boolean}}set player(t){this._player=t,this.hasProgress&&this.trackProgress()}get duration(){return this.player.mediaDuration}get player(){return this._player}get hasProgress(){return this.player.hasProgress}get width(){return this.shadowRoot.querySelector(".mmp-progress").offsetWidth}get offset(){return this.getBoundingClientRect().left}get classes(){return pt({transiting:!this.seekProgress,seeking:this.seekProgress})}render(){return z`
        <div
          class="mmp-progress"
          @touchstart=${this.initSeek}
          @touchend=${this.handleSeek}
          @mousedown=${this.initSeek}
          @mouseup=${this.handleSeek}
          @mouseleave=${this.resetSeek}
          @click=${t=>t.stopPropagation()}
          ?paused=${!this.player.isPlaying}
        >
          ${this.showTime?z`
                <div class="mmp-progress__duration">
                  <span
                    >${Xt(this.seekProgress||this.progress)}</span
                  >
                  <span>${Xt(this.duration)}</span>
                </div>
              `:""}
          <paper-progress
            class=${this.classes}
            value=${this.seekProgress||this.progress}
            max=${this.duration}
          >
          </paper-progress>
        </div>
      `}trackProgress(){this.progress=this.player.progress,this.tracker||(this.tracker=setInterval(()=>this.trackProgress(),1e3)),this.player.isPlaying||(clearInterval(this.tracker),this.tracker=null)}initSeek(t){const e=t.offsetX||t.touches[0].pageX-this.offset;this.seekWidth=this.width,this.seekProgress=this.calcProgress(e),this.addEventListener("touchmove",this.moveSeek),this.addEventListener("mousemove",this.moveSeek)}resetSeek(){this.seekProgress=null,this.removeEventListener("touchmove",this.moveSeek),this.removeEventListener("mousemove",this.moveSeek)}moveSeek(t){t.preventDefault();const e=t.offsetX||t.touches[0].pageX-this.offset;this.seekProgress=this.calcProgress(e)}handleSeek(t){this.resetSeek();const e=t.offsetX||t.changedTouches[0].pageX-this.offset,i=this.calcProgress(e);this.player.seek(t,i)}disconnectedCallback(){this.resetSeek(),clearInterval(this.tracker)}calcProgress(t){const e=t/this.seekWidth*this.duration;return Math.min(Math.max(e,.1),this.duration)}static get styles(){return nt`
        .mmp-progress {
          cursor: pointer;
          left: 0;
          right: 0;
          bottom: 0;
          position: absolute;
          pointer-events: auto;
          min-height: calc(var(--mmp-progress-height) + 10px);
        }
        .mmp-progress__duration {
          left: calc(var(--ha-card-border-radius, 4px) / 2);
          right: calc(var(--ha-card-border-radius, 4px) / 2);
          bottom: calc(var(--mmp-progress-height) + 6px);
          position: absolute;
          display: flex;
          justify-content: space-between;
          font-size: 0.8em;
          padding: 0 6px;
          z-index: 2;
        }
        paper-progress {
          height: var(--mmp-progress-height);
          --paper-progress-height: var(--mmp-progress-height);
          bottom: 0;
          position: absolute;
          width: 100%;
          transition: height 0;
          z-index: 1;
          --paper-progress-active-color: var(--mmp-accent-color);
          --paper-progress-container-color: rgba(100, 100, 100, 0.15);
          --paper-progress-transition-duration: 1s;
          --paper-progress-transition-timing-function: linear;
          --paper-progress-transition-delay: 0s;
        }
        paper-progress.seeking {
          transition: height 0.15s ease-out;
          height: calc(var(--mmp-progress-height) + 4px);
          --paper-progress-height: calc(var(--mmp-progress-height) + 4px);
        }
        .mmp-progress[paused] paper-progress {
          --paper-progress-active-color: var(
            --disabled-text-color,
            rgba(150, 150, 150, 0.5)
          );
        }`}}),customElements.define("mmp-source-menu",class extends ct{static get properties(){return{player:{},icon:Boolean}}get source(){return this.player.source}get sources(){return this.player.sources.map(t=>({name:t,id:t,type:"source"}))}render(){return z`
        <mmp-dropdown
          @change=${this.handleSource}
          .items=${this.sources}
          .label=${this.source}
          .selected=${this.source}
          .icon=${this.icon}
        ></mmp-dropdown>
      `}handleSource(t){const{id:e}=t.detail;this.player.setSource(t,e)}static get styles(){return nt`
        :host {
          max-width: 120px;
          min-width: var(--mmp-unit);
        }
        :host([full]) {
          max-width: none;
        }`}}),customElements.define("mmp-sound-menu",class extends ct{static get properties(){return{player:{},selected:String,icon:Boolean}}get mode(){return this.player.soundMode}get modes(){return this.player.soundModes.map(t=>({name:t,id:t,type:"soundMode"}))}render(){return z`
        <mmp-dropdown
          @change=${this.handleChange}
          .items=${this.modes}
          .label=${this.mode}
          .selected=${this.selected||this.mode}
          .icon=${this.icon}
        ></mmp-dropdown>
      `}handleChange(t){const{id:e}=t.detail;this.player.setSoundMode(t,e),this.selected=e}static get styles(){return nt`
        :host {
          max-width: 120px;
          min-width: var(--mmp-unit);
        }
        :host([full]) {
          max-width: none;
        }`}}),customElements.define("mmp-media-controls",class extends ct{static get properties(){return{player:{},config:{},break:Boolean}}get showShuffle(){return!this.config.hide.shuffle&&this.player.supportsShuffle}get maxVol(){return this.config.max_volume||100}get minVol(){return this.config.min_volume||0}render(){const{hide:t}=this.config;return z`
        ${t.volume?z``:this.renderVolControls(this.player.muted)}
        ${this.showShuffle?z`
              <div class="flex mmp-media-controls__shuffle">
                <paper-icon-button
                  class="shuffle-button"
                  @click=${t=>this.player.toggleShuffle(t)}
                  .icon=${Lt.SHUFFLE}
                  ?color=${this.player.shuffle}
                >
                </paper-icon-button>
              </div>
            `:z``}
        ${t.controls?z``:z`
              <div
                class="flex mmp-media-controls__media"
                ?flow=${this.config.flow||this.break}
              >
                <paper-icon-button
                  @click=${t=>this.player.prev(t)}
                  .icon=${Lt.PREV}
                >
                </paper-icon-button>
                ${this.renderPlayButtons()}
                <paper-icon-button
                  @click=${t=>this.player.next(t)}
                  .icon=${Lt.NEXT}
                >
                </paper-icon-button>
              </div>
            `}
      `}renderVolControls(t){return this.config.volume_stateless?this.renderVolButtons(t):this.renderVolSlider(t)}renderVolSlider(t){return z`
        <div class="mmp-media-controls__volume --slider flex">
          ${this.renderMuteButton(t)}
          <ha-slider
            @change=${this.handleVolumeChange}
            @click=${t=>t.stopPropagation()}
            ?disabled=${t}
            min=${this.minVol}
            max=${this.maxVol}
            value=${100*this.player.vol}
            dir=${"ltr"}
            ignore-bar-touch
            pin
          >
          </ha-slider>
        </div>
      `}renderVolButtons(t){return z`
        <div class="mmp-media-controls__volume --buttons flex">
          ${this.renderMuteButton(t)}
          <paper-icon-button
            @click=${t=>this.player.volumeDown(t)}
            .icon=${Lt.VOL_DOWN}
          >
          </paper-icon-button>
          <paper-icon-button
            @click=${t=>this.player.volumeUp(t)}
            .icon=${Lt.VOL_UP}
          >
          </paper-icon-button>
        </div>
      `}renderMuteButton(t){if(!this.config.hide.mute)switch(this.config.replace_mute){case"play":case"play_pause":return z`
            <paper-icon-button
              @click=${t=>this.player.playPause(t)}
              .icon=${Lt.PLAY[this.player.isPlaying]}
            >
            </paper-icon-button>
          `;case"stop":return z`
            <paper-icon-button
              @click=${t=>this.player.stop(t)}
              .icon=${Lt.STOP.true}
            >
            </paper-icon-button>
          `;case"play_stop":return z`
            <paper-icon-button
              @click=${t=>this.player.playStop(t)}
              .icon=${Lt.STOP[this.player.isPlaying]}
            >
            </paper-icon-button>
          `;case"next":return z`
            <paper-icon-button
              @click=${t=>this.player.next(t)}
              .icon=${Lt.NEXT}
            >
            </paper-icon-button>
          `;default:if(!this.player.supportsMute)return;return z`
            <paper-icon-button
              @click=${t=>this.player.toggleMute(t)}
              .icon=${Lt.MUTE[t]}
            >
            </paper-icon-button>
          `}}renderPlayButtons(){const{hide:t}=this.config;return z`
        ${t.play_pause?z``:z`
              <paper-icon-button
                @click=${t=>this.player.playPause(t)}
                .icon=${Lt.PLAY[this.player.isPlaying]}
              >
              </paper-icon-button>
            `}
        ${t.play_stop?z``:z`
              <paper-icon-button
                @click=${t=>this.handleStop(t)}
                .icon=${t.play_pause?Lt.STOP[this.player.isPlaying]:Lt.STOP.true}
              >
              </paper-icon-button>
            `}
      `}handleStop(t){return this.config.hide.play_pause?this.player.playStop(t):this.player.stop(t)}handleVolumeChange(t){const e=parseFloat(t.target.value)/100;this.player.setVolume(t,e)}static get styles(){return[Ft,nt`
          :host {
            display: flex;
            width: 100%;
            justify-content: space-between;
          }
          .flex {
            display: flex;
            flex: 1;
            justify-content: space-between;
          }
          ha-slider {
            max-width: none;
            min-width: 100px;
            width: 100%;
          }
          paper-icon-button {
            min-width: var(--mmp-unit);
          }
          .mmp-media-controls__volume {
            flex: 100;
            max-height: var(--mmp-unit);
          }
          .mmp-media-controls__volume.--buttons {
            justify-content: left;
          }
          .mmp-media-controls__media {
            margin-right: 0;
            margin-left: auto;
            justify-content: inherit;
          }
          .mmp-media-controls__media[flow] {
            max-width: none;
            justify-content: space-between;
          }
          .mmp-media-controls__shuffle {
            flex: 3;
            flex-shrink: 200;
            justify-content: center;
          }
          .mmp-media-controls__shuffle paper-icon-button {
            height: 36px;
            width: 36px;
            min-width: 36px;
            margin: 2px;
          }
        `]}});const Jt=(t,e,i="unknown")=>{const r=t.selectedLanguage||t.language,s=t.resources[r];return s&&s[e]?s[e]:i};customElements.define("mmp-powerstrip",class extends ct{static get properties(){return{hass:{},player:{},config:{},groupVisible:Boolean,idle:Boolean}}get icon(){return this.config.speaker_group.icon||Lt.GROUP}get showGroupButton(){return this.config.speaker_group.entities}get showPowerButton(){return!this.config.hide.power}get powerColor(){return this.player.active&&!this.config.hide.power_state}get sourceSize(){return"icon"===this.config.source||this.hasControls||this.idle}get soundSize(){return"icon"===this.config.sound_mode||this.hasControls||this.idle}get hasControls(){return this.player.active&&this.config.hide.controls!==this.config.hide.volume}get hasSource(){return this.player.sources.length>0&&!this.config.hide.source}get hasSoundMode(){return this.player.soundModes.length>0&&!this.config.hide.sound_mode}render(){return this.player.isUnavailable?z`
          <span class="label ellipsis">
            ${Jt(this.hass,"state.default.unavailable","Unavailable")}
          </span>
        `:z`
        ${this.idle?this.renderIdleView:""}
        ${this.hasControls?z`
              <mmp-media-controls .player=${this.player} .config=${this.config}>
              </mmp-media-controls>
            `:""}
        ${this.hasSource?z`
              <mmp-source-menu
                .player=${this.player}
                .icon=${this.sourceSize}
                ?full=${"full"===this.config.source}
              >
              </mmp-source-menu>
            `:""}
        ${this.hasSoundMode?z`
              <mmp-sound-menu
                .player=${this.player}
                .icon=${this.soundSize}
                ?full=${"full"===this.config.sound_mode}
              >
              </mmp-sound-menu>
            `:""}
        ${this.showGroupButton?z`
              <paper-icon-button
                class="group-button"
                .icon=${this.icon}
                ?inactive=${!this.player.isGrouped}
                ?color=${this.groupVisible}
                @click=${this.handleGroupClick}
              >
              </paper-icon-button>
            `:""}
        ${this.showPowerButton?z`
              <paper-icon-button
                class="power-button"
                .icon=${Lt.POWER}
                @click=${t=>this.player.toggle(t)}
                ?color=${this.powerColor}
              >
              </paper-icon-button>
            `:""}
      `}handleGroupClick(t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("toggleGroupList"))}get renderIdleView(){return this.player.isPaused?z`
          <paper-icon-button
            .icon=${Lt.PLAY[this.player.isPlaying]}
            @click=${t=>this.player.playPause(t)}
          >
          </paper-icon-button>
        `:z`
          <span class="label ellipsis">
            ${Jt(this.hass,"state.media_player.idle","Idle")}
          </span>
        `}static get styles(){return[Ft,nt`
          :host {
            display: flex;
            line-height: var(--mmp-unit);
            max-height: var(--mmp-unit);
          }
          :host([flow]) mmp-media-controls {
            max-width: unset;
          }
          mmp-media-controls {
            max-width: calc(var(--mmp-unit) * 5);
            line-height: initial;
            justify-content: flex-end;
          }
          .group-button {
            height: calc(var(--mmp-unit) * 0.85);
            width: calc(var(--mmp-unit) * 0.85);
            min-width: calc(var(--mmp-unit) * 0.85);
            margin: 3px;
          }
          paper-icon-button {
            min-width: var(--mmp-unit);
          }
        `]}}),customElements.get("ha-slider")||customElements.define("ha-slider",class extends(customElements.get("paper-slider")){}),customElements.define("hui-ais-mini-media-player-card",class extends ct{constructor(){super(),this._overflow=!1,this.initial=!0,this.picture=!1,this.thumbnail=!1,this.edit=!1,this.rtl=!1}static get properties(){return{_hass:{},config:{},entity:{},player:{},_overflow:Boolean,break:Boolean,initial:Boolean,picture:String,thumbnail:String,edit:Boolean,rtl:Boolean,idle:Boolean}}static get styles(){return[Ft,Ht]}set hass(t){if(!t)return;const e=t.states[this.config.entity];this._hass=t,e&&this.entity!==e&&(this.entity=e,this.player=new qt(t,this.config,e),this.rtl=this.computeRTL(t),this.idle=this.player.idle,this.player.trackIdle&&this.updateIdleStatus());const i=Object.keys(t.states);let r;for(this.ais_speaker_group_entities=[],r=0;r<i.length;r+=1)if(i[r].startsWith("media_player.")){const e=t.states[i[r]].attributes;this.ais_speaker_group_entities.push({entity_id:t.states[i[r]].entity_id,name:e.friendly_name||"Głośnik"})}this.config.speaker_group.show_group_count=!0,this.config.speaker_group.platform="ais_exo_player",this.config.speaker_group.entities=this.ais_speaker_group_entities}get hass(){return this._hass}set overflow(t){this._overflow!==t&&(this._overflow=t)}get overflow(){return this._overflow}get name(){return this.config.name||this.player.name}setConfig(t){if(!t.entity||"media_player"!==t.entity.split(".")[0])throw new Error("Specify an entity from within the media_player domain.");const e=Object.assign({artwork:"default",info:"default",more_info:!0,source:"default",sound_mode:"default",toggle_power:!0,tap_action:{action:"more-info"}},t,{hide:Object.assign({},jt,{},t.hide),speaker_group:Object.assign({show_group_count:!0,platform:"sonos"},t.sonos,{},t.speaker_group),shortcuts:Object.assign({label:Wt},t.shortcuts)});e.max_volume=Number(e.max_volume)||100,e.min_volume=Number(e.min_volume)||0,e.collapse=e.hide.controls||e.hide.volume,e.info=e.collapse&&"scroll"!==e.info?"short":e.info,e.flow=e.hide.icon&&e.hide.name&&e.hide.info,this.config=e}shouldUpdate(t){return void 0===this.break&&this.computeRect(this),Bt.some(e=>t.has(e))&&this.player}firstUpdated(){new Rt(t=>{t.forEach(t=>{window.requestAnimationFrame(()=>{"scroll"===this.config.info&&this.computeOverflow(),this._resizeTimer||(this.computeRect(t),this._resizeTimer=setTimeout(()=>{this._resizeTimer=null,this.computeRect(this._resizeEntry)},250)),this._resizeEntry=t})})}).observe(this),setTimeout(()=>this.initial=!1,250),this.edit=this.config.speaker_group.expanded||!1}updated(){"scroll"===this.config.info&&setTimeout(()=>{this.computeOverflow()},10)}render({config:t}=this){const e=this.computeArtwork();return z`
        <ha-card
          class=${this.computeClasses()}
          style=${this.computeStyles()}
          @click=${t=>this.handlePopup(t)}
          artwork=${t.artwork}
          content=${this.player.content}
        >
          <div class="mmp__bg">
            ${this.renderArtwork(e)}
          </div>
          <div class="mmp-player">
            <div class="mmp-player__core flex" ?inactive=${this.player.idle}>
              ${this.renderIcon(e)}
              <div class="entity__info">
                ${this.renderEntityName()} ${this.renderMediaInfo()}
              </div>
              <mmp-powerstrip
                @toggleGroupList=${this.toggleGroupList}
                .hass=${this.hass}
                .player=${this.player}
                .config=${t}
                .groupVisible=${this.edit}
                .idle=${this.idle}
                ?flow=${t.flow}
              >
              </mmp-powerstrip>
            </div>
            <div class="mmp-player__adds">
              ${!t.collapse&&this.player.active?z`
                    <mmp-media-controls
                      .player=${this.player}
                      .config=${t}
                      .break=${this.break}
                    >
                    </mmp-media-controls>
                  `:""}
              <mmp-shortcuts
                .player=${this.player}
                .hass=${this.hass}
                .shortcuts=${t.shortcuts}
              >
              </mmp-shortcuts>
              ${t.tts?z`
                    <mmp-tts
                      .config=${t.tts}
                      .hass=${this.hass}
                      .entity=${this.player.id}
                    >
                    </mmp-tts>
                  `:""}
              <mmp-group-list
                .visible=${this.edit}
                .entities=${t.speaker_group.entities}
                .player=${this.player}
              >
              </mmp-group-list>
            </div>
          </div>
          <div class="mmp__container">
            ${this.player.active&&this.player.hasProgress?z`
                  <mmp-progress
                    .player=${this.player}
                    .showTime=${!this.config.hide.runtime}
                  >
                  </mmp-progress>
                `:""}
          </div>
        </ha-card>
      `}renderArtwork(t){if(!this.thumbnail&&!this.config.background)return;const e=!this.config.background||t&&"default"!==this.config.artwork?this.thumbnail:`url(${this.config.background})`;return z`
        <div class="cover" style="background-image: ${e};"></div>
      `}handlePopup(t){t.stopPropagation(),Gt(this,this._hass,this.config,this.config.tap_action,this.player.id)}renderIcon(t){if(this.config.hide.icon)return;if(this.player.active&&t&&"default"===this.config.artwork)return z`
          <div
            class="entity__artwork"
            style="background-image: ${this.thumbnail};"
            ?border=${!this.config.hide.artwork_border}
            state=${this.player.state}
          ></div>
        `;const e=!this.config.hide.icon_state&&this.player.isActive;return z`
        <div class="entity__icon" ?color=${e}>
          <ha-icon .icon=${this.computeIcon()}></ha-icon>
        </div>
      `}renderEntityName(){if(!this.config.hide.name)return z`
        <div class="entity__info__name">
          ${this.name} ${this.speakerCount()}
        </div>
      `}renderMediaInfo(){if(this.config.hide.info)return;const t=this.player.mediaInfo;return z`
        <div
          class="entity__info__media"
          ?short=${"short"===this.config.info||!this.player.active}
          ?short-scroll=${"scroll"===this.config.info}
          ?scroll=${this.overflow}
          style="animation-duration: ${this.overflow}s;"
        >
          ${"scroll"===this.config.info?z`
                <div>
                  <div class="marquee">
                    ${t.map(t=>z`
                          <span class=${`attr__${t.attr}`}
                            >${t.prefix+t.text}</span
                          >
                        `)}
                  </div>
                </div>
              `:""}
          ${t.map(t=>z`
                <span class=${`attr__${t.attr}`}>${t.prefix+t.text}</span>
              `)}
        </div>
      `}speakerCount(){if(this.config.speaker_group.show_group_count){const t=this.player.groupCount;return t>1?` +${t-1}`:""}}computeClasses({config:t}=this){return pt({"--responsive":this.break||t.hide.icon,"--initial":this.initial,"--bg":t.background,"--group":t.group,"--more-info":"none"!==t.tap_action,"--has-artwork":this.player.hasArtwork&&this.thumbnail,"--flow":t.flow,"--collapse":t.collapse,"--rtl":this.rtl,"--progress":this.player.hasProgress,"--runtime":!t.hide.runtime&&this.player.hasProgress,"--inactive":!this.player.isActive})}computeStyles(){const{scale:t}=this.config;return dt(Object.assign({},t&&{"--mmp-unit":`${40*t}px`}))}computeArtwork(){const{picture:t,hasArtwork:e}=this.player;return e&&t!==this.picture&&(this.thumbnail=this.player.artwork,this.picture=t),!(!e||!this.thumbnail)}computeIcon(){return this.config.icon?this.config.icon:this.player.icon||Lt.DEFAULT}computeOverflow(){const t=this.shadowRoot.querySelector(".marquee");if(t){const e=t.clientWidth>t.parentNode.clientWidth;this.overflow=!(!e||!this.player.active)&&7.5+t.clientWidth/50}}computeRect(t){const{left:e,width:i}=t.contentRect||t.getBoundingClientRect();this.break=i+2*e<It}computeRTL(t){const e=t.language||"en";return t.translationMetadata.translations[e]&&t.translationMetadata.translations[e].isRTL||!1}toggleGroupList(){this.edit=!this.edit}fire(t,e,i){const r=i||{},s=null==e?{}:e,o=new Event(t,{bubbles:void 0===r.bubbles||r.bubbles,cancelable:Boolean(r.cancelable),composed:void 0===r.composed||r.composed});return o.detail=s,this.dispatchEvent(o),o}updateIdleStatus(){this._idleTracker&&clearTimeout(this._idleTracker);const t=(Date.now()-new Date(this.player.updatedAt).getTime())/1e3;this._idleTracker=setTimeout(()=>{this.idle=this.player.checkIdleAfter(this.config.idle_view.after),this.player.idle=this.idle,this._idleTracker=null},1e3*(60*this.config.idle_view.after-t))}getCardSize(){return this.config.collapse?1:2}})})()}).call(this,i(290))}}]);
//# sourceMappingURL=chunk.9cb9e16821a19528b908.js.map