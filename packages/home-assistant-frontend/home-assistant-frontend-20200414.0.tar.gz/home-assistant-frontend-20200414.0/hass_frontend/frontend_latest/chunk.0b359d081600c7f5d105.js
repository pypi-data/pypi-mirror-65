(self.webpackJsonp=self.webpackJsonp||[]).push([[216],{819:function(e,t,r){"use strict";r.r(t),r.d(t,"severityMap",function(){return k});var i=r(0),n=r(217),a=r(89),o=r(11),s=r(188),c=r(298),l=(r(189),r(255)),d=r(210);r(211);function u(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function y(e,t,r){return(y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=b(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function b(e){return(b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const k={red:"var(--label-badge-red)",green:"var(--label-badge-green)",yellow:"var(--label-badge-yellow)",normal:"var(--label-badge-blue)"};!function(e,t,r,i){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[a])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=m(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t(function(e){n.initializeInstanceElements(e,s.elements)},r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if(p(a.descriptor)||p(n.descriptor)){if(h(a)||h(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(h(a)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}f(a,n)}else t.push(a)}return t}(o.d.map(u)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([Object(i.d)("hui-gauge-card")],function(e,t){class u extends t{constructor(...t){super(...t),e(this)}}return{F:u,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(4),r.e(145),r.e(11),r.e(68)]).then(r.bind(null,779)),document.createElement("hui-gauge-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,r){return{type:"gauge",entity:Object(l.a)(e,1,t,r,["sensor"],e=>!isNaN(Number(e.state)))[0]||""}}},{kind:"field",decorators:[Object(i.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_baseUnit",value:()=>"50px"},{kind:"field",decorators:[Object(i.g)()],key:"_config",value:void 0},{kind:"field",key:"_updated",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 2}},{kind:"method",key:"setConfig",value:function(e){if(!e||!e.entity)throw new Error("Invalid card configuration");if(!Object(c.b)(e.entity))throw new Error("Invalid Entity");this._config=Object.assign({min:0,max:100},e)}},{kind:"method",key:"connectedCallback",value:function(){y(b(u.prototype),"connectedCallback",this).call(this),this._setBaseUnit()}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return i.f``;const e=this.hass.states[this._config.entity];if(!e)return i.f`
        <hui-warning
          >${this.hass.localize("ui.panel.lovelace.warning.entity_not_found","entity",this._config.entity)}</hui-warning
        >
      `;const t=Number(e.state);return isNaN(t)?i.f`
        <hui-warning
          >${this.hass.localize("ui.panel.lovelace.warning.entity_non_numeric","entity",this._config.entity)}</hui-warning
        >
      `:i.f`
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
    `}},{kind:"method",key:"shouldUpdate",value:function(e){return Object(d.a)(this,e)}},{kind:"method",key:"firstUpdated",value:function(){this._updated=!0,this._setBaseUnit(),this.classList.add("init")}},{kind:"method",key:"updated",value:function(e){if(y(b(u.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),r=e.get("_config");t&&r&&t.themes===this.hass.themes&&r.theme===this._config.theme||Object(a.a)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_setBaseUnit",value:function(){if(!this.isConnected||!this._updated)return;const e=this._computeBaseUnit();"0px"!==e&&(this._baseUnit=e)}},{kind:"method",key:"_computeSeverity",value:function(e){const t=this._config.severity;if(!t)return k.normal;const r=Object.keys(t).map(e=>[e,t[e]]);for(const i of r)if(null==k[i[0]]||isNaN(i[1]))return k.normal;return r.sort((e,t)=>e[1]-t[1]),e>=r[0][1]&&e<r[1][1]?k[r[0][0]]:e>=r[1][1]&&e<r[2][1]?k[r[1][0]]:e>=r[2][1]?k[r[2][0]]:k.normal}},{kind:"method",key:"_translateTurn",value:function(e){const{min:t,max:r}=this._config;return 5*(Math.min(Math.max(e,t),r)-t)/(r-t)/10}},{kind:"method",key:"_computeBaseUnit",value:function(){return this.clientWidth<200?this.clientWidth/5+"px":"50px"}},{kind:"method",key:"_handleClick",value:function(){Object(o.a)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
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
    `}}]}},i.a)}}]);
//# sourceMappingURL=chunk.0b359d081600c7f5d105.js.map