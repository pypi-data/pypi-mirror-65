(self.webpackJsonp=self.webpackJsonp||[]).push([[16],{191:function(t,e,a){"use strict";var i=a(8);e.a=Object(i.a)(t=>(class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},229:function(t,e,a){"use strict";a.d(e,"a",function(){return i}),a.d(e,"c",function(){return s}),a.d(e,"b",function(){return n});const i=function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}return!1}(),s=function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}return!1}(),n=function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}return!1}()},240:function(t,e,a){"use strict";a.d(e,"a",function(){return n}),a.d(e,"b",function(){return r});var i=a(225),s=a(229);const n=s.b?(t,e)=>t.toLocaleString(e,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):t=>i.a.format(t,`${i.a.masks.longDate}, ${i.a.masks.shortTime}`),r=s.b?(t,e)=>t.toLocaleString(e,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit"}):t=>i.a.format(t,`${i.a.masks.longDate}, ${i.a.masks.mediumTime}`)},255:function(t,e,a){"use strict";a.d(e,"a",function(){return n}),a.d(e,"b",function(){return r});var i=a(225),s=a(229);const n=s.c?(t,e)=>t.toLocaleTimeString(e,{hour:"numeric",minute:"2-digit"}):t=>i.a.format(t,"shortTime"),r=s.c?(t,e)=>t.toLocaleTimeString(e,{hour:"numeric",minute:"2-digit",second:"2-digit"}):t=>i.a.format(t,"mediumTime")},351:function(t,e,a){"use strict";a(204);var i=a(4),s=a(32),n=a(22),r=a(109),o=(a(119),a(11)),l=a(79),c=a(255);let h=null;customElements.define("ha-chart-base",class extends(Object(l.b)([r.a],s.a)){static get template(){return i.a`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        paper-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=(()=>{this._debouncer=n.a.debounce(this._debouncer,o.d.after(10),()=>{this._isAttached&&this.resizeChart()})}),"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver(t=>{t.forEach(()=>{this._resizeListener()})}),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===h&&(h=Promise.all([a.e(17),a.e(176),a.e(90)]).then(a.bind(null,871))),h.then(t=>{this.ChartClass=t.default,this.onPropsChange()})}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(t){if(0===t.opacity)return void this.set(["tooltip","opacity"],0);t.yAlign?this.set(["tooltip","yAlign"],t.yAlign):this.set(["tooltip","yAlign"],"no-transform");const e=t.title&&t.title[0]||"";this.set(["tooltip","title"],e);const a=t.body.map(t=>t.lines);t.body&&this.set(["tooltip","lines"],a.map((e,a)=>{const i=t.labelColors[a];return{color:i.borderColor,bgColor:i.backgroundColor,text:e.join("\n")}}));const i=this.$.chartTarget.clientWidth;let s=t.caretX;const n=this._chart.canvas.offsetTop+t.caretY;t.caretX+100>i?s=i-100:t.caretX<100&&(s=100),s+=this._chart.canvas.offsetLeft,this.tooltip=Object.assign({},this.tooltip,{opacity:1,left:`${s}px`,top:`${n}px`})}_legendClick(t){(t=t||window.event).stopPropagation();let e=t.target||t.srcElement;for(;"LI"!==e.nodeName;)e=e.parentElement;const a=t.model.itemsIndex,i=this._chart.getDatasetMeta(a);i.hidden=null===i.hidden?!this._chart.data.datasets[a].hidden:null,this.set(["metas",a,"hidden"],this._chart.isDatasetVisible(a)?null:"hidden"),this._chart.update()}_drawLegend(){const t=this._chart,e=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map((a,i)=>({label:a.label,color:a.color,bgColor:a.backgroundColor,hidden:e&&i<this.metas.length?this.metas[i].hidden:!t.isDatasetVisible(i)})));let a=!1;if(e)for(let i=0;i<this.metas.length;i++){const e=t.getDatasetMeta(i);!!e.hidden!=!!this.metas[i].hidden&&(a=!0),e.hidden=!!this.metas[i].hidden||null}a&&t.update(),this.unit=this.data.unit}_formatTickValue(t,e,a){if(0===a.length)return t;const i=new Date(a[e].value);return Object(c.a)(i)}drawChart(){const t=this.data.data,e=this.$.chartCanvas;if(t.datasets&&t.datasets.length||this._chart){if("timeline"!==this.data.type&&t.datasets.length>0){const e=t.datasets.length,a=this.constructor.getColorList(e);for(let i=0;i<e;i++)t.datasets[i].borderColor=a[i].rgbString(),t.datasets[i].backgroundColor=a[i].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=t,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=t.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!t.datasets)return;this._customTooltips({opacity:0});const a=[{afterRender:()=>this._setRendered(!0)}];let i={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};(i=Chart.helpers.merge(i,this.data.options)).scales.xAxes[0].ticks.callback=this._formatTickValue,"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(i.elements.colorFunction=this._colorFunc),1===t.datasets.length&&(i.scales.yAxes[0].ticks?i.scales.yAxes[0].ticks.display=!1:i.scales.yAxes[0].ticks={display:!1},i.scales.yAxes[0].gridLines?i.scales.yAxes[0].gridLines.display=!1:i.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const s={type:this.data.type,data:this.data.data,options:i,plugins:a};this._chart=new this.ChartClass(e,s),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const t=this.$.chartTarget,e=this.data.data;if(0===e.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const a=this._chart.chartArea.top,i=this._chart.chartArea.bottom,s=this._chart.canvas.clientHeight;if(i>0&&(this._axisHeight=s-i+a),!this._axisHeight)return t.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const a=30*e.datasets.length+this._axisHeight+"px";t.style.height!==a&&(t.style.height=a),this._chart.resize()}}static getColorList(t){let e=!1;t>10&&(e=!0,t=Math.ceil(t/2));const a=360/t,i=[];for(let s=0;s<t;s++)i[s]=Color().hsl(a*s,80,38),e&&(i[s+t]=Color().hsl(a*s,80,62));return i}static getColorGenerator(t,e){const a=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function i(t){return Color("#"+a[t%a.length])}const s={};let n=0;return e>0&&(n=e),t&&Object.keys(t).forEach(e=>{const a=t[e];isFinite(a)?s[e.toLowerCase()]=i(a):s[e.toLowerCase()]=Color(t[e])}),function(t,e){let a;const r=e[3];if(null===r)return Color().hsl(0,40,38);if(void 0===r)return Color().hsl(120,40,38);const o=r.toLowerCase();return void 0===a&&(a=s[o]),void 0===a&&(a=i(n),n++,s[o]=a),a}}});var d=a(191),u=a(240);customElements.define("state-history-chart-line",class extends(Object(d.a)(s.a)){static get template(){return i.a`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}_onRenderedChanged(t){t&&this.animateHeight()}animateHeight(){requestAnimationFrame(()=>requestAnimationFrame(()=>{this.style.height=this.$.chart.scrollHeight+"px"}))}drawChart(){const t=this.unit,e=this.data,a=[];let i;if(!this._isAttached)return;if(0===e.length)return;function s(t){const e=parseFloat(t);return isFinite(e)?e:null}(i=this.endTime||new Date(Math.max.apply(null,e.map(t=>new Date(t.states[t.states.length-1].last_changed)))))>new Date&&(i=new Date);const n=this.names||{};e.forEach(e=>{const r=e.domain,o=n[e.entity_id]||e.name;let l;const c=[];function h(t,e){e&&(t>i||(c.forEach((a,i)=>{a.data.push({x:t,y:e[i]})}),l=e))}function d(e,a,i){let s=!1,n=!1;i&&(s="origin"),a&&(n="before"),c.push({label:e,fill:s,steppedLine:n,pointRadius:0,data:[],unitText:t})}if("thermostat"===r||"climate"===r||"water_heater"===r){const t=e.states.some(t=>t.attributes&&t.attributes.hvac_action),a="climate"===r&&t?t=>"heating"===t.attributes.hvac_action:t=>"heat"===t.state,i="climate"===r&&t?t=>"cooling"===t.attributes.hvac_action:t=>"cool"===t.state,n=e.states.some(a),l=e.states.some(i),c=e.states.some(t=>t.attributes&&t.attributes.target_temp_high!==t.attributes.target_temp_low);d(`${this.hass.localize("ui.card.climate.current_temperature","name",o)}`,!0),n&&d(`${this.hass.localize("ui.card.climate.heating","name",o)}`,!0,!0),l&&d(`${this.hass.localize("ui.card.climate.cooling","name",o)}`,!0,!0),c?(d(`${this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.high"))}`,!0),d(`${this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.low"))}`,!0)):d(`${this.hass.localize("ui.card.climate.target_temperature_entity","name",o)}`,!0),e.states.forEach(t=>{if(!t.attributes)return;const e=s(t.attributes.current_temperature),r=[e];if(n&&r.push(a(t)?e:null),l&&r.push(i(t)?e:null),c){const e=s(t.attributes.target_temp_high),a=s(t.attributes.target_temp_low);r.push(e,a),h(new Date(t.last_changed),r)}else{const e=s(t.attributes.temperature);r.push(e),h(new Date(t.last_changed),r)}})}else{d(o,"sensor"===r);let t=null,a=null,i=null;e.states.forEach(e=>{const n=s(e.state),r=new Date(e.last_changed);if(null!==n&&null!==i){const e=r.getTime(),s=i.getTime(),o=a.getTime();h(i,[(s-o)/(e-o)*(n-t)+t]),h(new Date(s+1),[null]),h(r,[n]),a=r,t=n,i=null}else null!==n&&null===i?(h(r,[n]),a=r,t=n):null===n&&null===i&&null!==t&&(i=r)})}h(i,l),Array.prototype.push.apply(a,c)});const r={type:"line",unit:t,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(t,e)=>{const a=t[0],i=e.datasets[a.datasetIndex].data[a.index].x;return Object(u.b)(i,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:a}};this.chartData=r}});var m=a(108);customElements.define("state-history-chart-timeline",class extends(Object(d.a)(s.a)){static get template(){return i.a`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let t=this.data;if(!this._isAttached)return;t||(t=[]);const e=new Date(t.reduce((t,e)=>Math.min(t,new Date(e.data[0].last_changed)),new Date));let a=this.endTime||new Date(t.reduce((t,e)=>Math.max(t,new Date(e.data[e.data.length-1].last_changed)),e));a>new Date&&(a=new Date);const i=[],s=[],n=this.names||{};t.forEach(t=>{let r,o=null,l=null,c=e;const h=n[t.entity_id]||t.name,d=[];t.data.forEach(t=>{let e=t.state;void 0!==e&&""!==e||(e=null),new Date(t.last_changed)>a||(null!==o&&e!==o?(r=new Date(t.last_changed),d.push([c,r,l,o]),o=e,l=t.state_localize,c=r):null===o&&(o=e,l=t.state_localize,c=new Date(t.last_changed)))}),null!==o&&d.push([c,a,l,o]),s.push({data:d}),i.push(h)});const r={type:"timeline",options:{tooltips:{callbacks:{label:(t,e)=>{const a=e.datasets[t.datasetIndex].data[t.index],i=Object(u.b)(a[0],this.hass.language),s=Object(u.b)(a[1],this.hass.language);return[a[2],i,s]}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:t=>{t.maxWidth=.18*t.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:i,datasets:s},colors:{staticColors:{on:1,off:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=r}_computeRTL(t){return Object(m.a)(t)}});customElements.define("state-history-charts",class extends(Object(d.a)(s.a)){static get template(){return i.a`
      <style>
        :host {
          display: block;
          /* height of single timeline chart = 58px */
          min-height: 58px;
        }
        .info {
          text-align: center;
          line-height: 58px;
          color: var(--secondary-text-color);
        }
      </style>
      <template
        is="dom-if"
        class="info"
        if="[[_computeIsLoading(isLoadingData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.loading_history')]]
        </div>
      </template>

      <template
        is="dom-if"
        class="info"
        if="[[_computeIsEmpty(isLoadingData, historyData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.no_history_found')]]
        </div>
      </template>

      <template is="dom-if" if="[[historyData.timeline.length]]">
        <state-history-chart-timeline
          hass="[[hass]]"
          data="[[historyData.timeline]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          no-single="[[noSingle]]"
          names="[[names]]"
        ></state-history-chart-timeline>
      </template>

      <template is="dom-repeat" items="[[historyData.line]]">
        <state-history-chart-line
          hass="[[hass]]"
          unit="[[item.unit]]"
          data="[[item.data]]"
          identifier="[[item.identifier]]"
          is-single-device="[[_computeIsSingleLineChart(item.data, noSingle)]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          names="[[names]]"
        ></state-history-chart-line>
      </template>
    `}static get properties(){return{hass:Object,historyData:{type:Object,value:null},names:Object,isLoadingData:Boolean,endTime:{type:Object},upToNow:Boolean,noSingle:Boolean}}_computeIsSingleLineChart(t,e){return!e&&t&&1===t.length}_computeIsEmpty(t,e){const a=!e||!e.timeline||!e.line||0===e.timeline.length&&0===e.line.length;return!t&&a}_computeIsLoading(t){return t&&!this.historyData}_computeEndTime(t,e){return e?new Date:t}})}}]);
//# sourceMappingURL=chunk.551c087cba25a6fcd3c9.js.map