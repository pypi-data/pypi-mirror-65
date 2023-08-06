(self.webpackJsonp=self.webpackJsonp||[]).push([[216],{815:function(e,t,i){"use strict";i.r(t),i.d(t,"severityMap",function(){return b});var r=i(0),n=i(215),a=(i(189),i(211),i(294)),o=i(89),s=i(187),c=i(11),l=i(210),d=i(255);function u(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t,i){return(g="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const b={red:"var(--label-badge-red)",green:"var(--label-badge-green)",yellow:"var(--label-badge-yellow)",normal:"var(--label-badge-blue)"};!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var a="static"===n?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[a])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=m(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=m(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var a=0;a<r.length;a++)n=r[a](n);var o=t(function(e){n.initializeInstanceElements(e,s.elements)},i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var n,a=e[r];if("method"===a.kind&&(n=t.find(i)))if(p(a.descriptor)||p(n.descriptor)){if(h(a)||h(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(h(a)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}f(a,n)}else t.push(a)}return t}(o.d.map(u)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([Object(r.d)("hui-gauge-card")],function(e,t){class u extends t{constructor(...t){super(...t),e(this)}}return{F:u,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([i.e(4),i.e(145),i.e(11),i.e(68)]).then(i.bind(null,780)),document.createElement("hui-gauge-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i){return{type:"gauge",entity:Object(d.a)(e,1,t,i,["sensor"],e=>!isNaN(Number(e.state)))[0]||""}}},{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_baseUnit",value:()=>"50px"},{kind:"field",decorators:[Object(r.g)()],key:"_config",value:void 0},{kind:"field",key:"_updated",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 2}},{kind:"method",key:"setConfig",value:function(e){if(!e||!e.entity)throw new Error("Invalid card configuration");if(!Object(a.b)(e.entity))throw new Error("Invalid Entity");this._config=Object.assign({min:0,max:100},e)}},{kind:"method",key:"connectedCallback",value:function(){g(y(u.prototype),"connectedCallback",this).call(this),this._setBaseUnit()}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return r.f``;const e=this.hass.states[this._config.entity];if(!e)return r.f`
        <hui-warning
          >${this.hass.localize("ui.panel.lovelace.warning.entity_not_found","entity",this._config.entity)}</hui-warning
        >
      `;const t=Number(e.state);return isNaN(t)?r.f`
        <hui-warning
          >${this.hass.localize("ui.panel.lovelace.warning.entity_non_numeric","entity",this._config.entity)}</hui-warning
        >
      `:r.f`
      <ha-card
        @click="${this._handleClick}"
        tabindex="0"
        style=${Object(n.a)({"--base-unit":this._baseUnit})}
      >
        <div class="container">
          <div class="gauge-a"></div>
          <div
            class="gauge-c"
            style=${Object(n.a)({transform:`rotate(${this._translateTurn(t)}turn)`,"background-color":this._computeSeverity(t)})}
          ></div>
          <div class="gauge-b"></div>
        </div>
        <div class="gauge-data">
          <div id="percent">
            ${e.state}
            ${this._config.unit||e.attributes.unit_of_measurement||""}
          </div>
          <div id="name">
            ${this._config.name||Object(s.a)(e)}
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"shouldUpdate",value:function(e){return Object(l.a)(this,e)}},{kind:"method",key:"firstUpdated",value:function(){this._updated=!0,this._setBaseUnit(),this.classList.add("init")}},{kind:"method",key:"updated",value:function(e){if(g(y(u.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),i=e.get("_config");t&&i&&t.themes===this.hass.themes&&i.theme===this._config.theme||Object(o.a)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_setBaseUnit",value:function(){if(!this.isConnected||!this._updated)return;const e=this._computeBaseUnit();"0px"!==e&&(this._baseUnit=e)}},{kind:"method",key:"_computeSeverity",value:function(e){const t=this._config.severity;if(!t)return b.normal;const i=Object.keys(t).map(e=>[e,t[e]]);for(const r of i)if(null==b[r[0]]||isNaN(r[1]))return b.normal;return i.sort((e,t)=>e[1]-t[1]),e>=i[0][1]&&e<i[1][1]?b[i[0][0]]:e>=i[1][1]&&e<i[2][1]?b[i[1][0]]:e>=i[2][1]?b[i[2][0]]:b.normal}},{kind:"method",key:"_translateTurn",value:function(e){const{min:t,max:i}=this._config;return 5*(Math.min(Math.max(e,t),i)-t)/(i-t)/10}},{kind:"method",key:"_computeBaseUnit",value:function(){return this.clientWidth<200?this.clientWidth/5+"px":"50px"}},{kind:"method",key:"_handleClick",value:function(){Object(c.a)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      ha-card {
        cursor: pointer;
        padding: 16px 16px 0 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        justify-content: center;
        align-items: center;
      }
      ha-card:focus {
        outline: none;
        background: var(--divider-color);
      }
      .container {
        width: calc(var(--base-unit) * 4);
        height: calc(var(--base-unit) * 2);
        overflow: hidden;
        position: relative;
      }
      .gauge-a {
        position: absolute;
        background-color: var(--primary-background-color);
        width: calc(var(--base-unit) * 4);
        height: calc(var(--base-unit) * 2);
        top: 0%;
        border-radius: calc(var(--base-unit) * 2.5) calc(var(--base-unit) * 2.5)
          0px 0px;
      }
      .gauge-b {
        position: absolute;
        background-color: var(--paper-card-background-color);
        width: calc(var(--base-unit) * 2.5);
        height: calc(var(--base-unit) * 1.25);
        top: calc(var(--base-unit) * 0.75);
        margin-left: calc(var(--base-unit) * 0.75);
        margin-right: auto;
        border-radius: calc(var(--base-unit) * 2.5) calc(var(--base-unit) * 2.5)
          0px 0px;
      }
      .gauge-c {
        position: absolute;
        background-color: var(--label-badge-blue);
        width: calc(var(--base-unit) * 4);
        height: calc(var(--base-unit) * 2);
        top: calc(var(--base-unit) * 2);
        margin-left: auto;
        margin-right: auto;
        border-radius: 0px 0px calc(var(--base-unit) * 2)
          calc(var(--base-unit) * 2);
        transform-origin: center top;
      }
      .init .gauge-c {
        transition: all 1.3s ease-in-out;
      }
      .gauge-data {
        text-align: center;
        color: var(--primary-text-color);
        line-height: calc(var(--base-unit) * 0.3);
        width: 100%;
        position: relative;
        top: calc(var(--base-unit) * -0.5);
      }
      .init .gauge-data {
        transition: all 1s ease-out;
      }
      .gauge-data #percent {
        font-size: calc(var(--base-unit) * 0.55);
        line-height: calc(var(--base-unit) * 0.55);
      }
      .gauge-data #name {
        padding-top: calc(var(--base-unit) * 0.15);
        font-size: calc(var(--base-unit) * 0.3);
      }
    `}}]}},r.a)}}]);
//# sourceMappingURL=chunk.765fc2003871d55cbaee.js.map