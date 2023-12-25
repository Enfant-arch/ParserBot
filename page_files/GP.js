(function(d, w) {
	function getSrcGP() {
		var scriptList = document.querySelectorAll('script');
		var srcList = [];

		scriptList.forEach(function(item) {
			if (/\/GP.js$/.test(item.src)) {
				srcList.push(item.src);
			}
		});

		if (srcList.length === 1) {
		    return srcList[0];
		};
		return '';
	};
	function isObject(val){
		return typeof val === 'object' &&
			!Array.isArray(val) &&
			val !== null
	};
	function GeneralPixel(options) {
		var _this = this;
		this.options = {};
		this.rtgMessage = {};
		this.push = function(options) {
			for (var key in options) {
				this.options[key] = options[key];
			}
			checkOptions(this.options);
		};
		function checkOptions(options) {
			if (options.type === 'GPID') {
				getGrid(options);
			}
		}
		function getGrid(options) {
			var domain = /-src/.test(getSrcGP())
				? 'https://static-src.terratraf.io/GP/'
				: 'https://static.terratraf.io/GP/';

			var url = domain + options.id + '.js';
			var scripts = document.getElementsByTagName('script');
			if (scripts.length) {
				for (var i = 0; i < scripts.length; i++) {
					if (scripts.item(i).src && scripts.item(i).src.indexOf(url) + 1) {
						return null;
					}
				}
			}
			var s = d.createElement('script');
			s.src = url;
			d.head.appendChild(s);
		}
		this.push(options);

		this.dataForRTGMessage = [];

		this.sendRTGMessage = function(data){
			if(!data){
				data = isObject(_this.rtgMessage)?{..._this.rtgMessage}:null;
				_this.rtgMessage={};
			};
			if(!isObject(data)){
				console.error("Error:sendData The parameter is not an object");
				return;
			};

			if (!data.action){
				console.error("Error:sendData action parameter is required");
				return;
			};

			_this.dataForRTGMessage.push(data);

		}

	}
	var options = {};
	if (!w.generalPixel) {
		w.generalPixel = new GeneralPixel(options);
	}
	if (Array.isArray(w.generalPixel)) {
		w.generalPixel.forEach(function(item) {
			for (var key in item) {
				options[key] = item[key];
			}
		});
	}
	if (!w.generalPixel.options) {
		w.generalPixel = new GeneralPixel(options);
	}
})(document, window);
//old 29.11.19
(function(d, w) {
	function FfData(options) {
		this.options = {};
		this.push = function(options) {
			for (var key in options) {
				this.options[key] = options[key];
			}
			checkOptions(this.options);
		};
		function checkOptions(options) {
			if (options.type === 'GPID') {
				getGrid(options);
			}
		}
		function getGrid(options) {
			var url = 'https://pix.sniperlog.ru/GP/' + options.id + '.js';
			var scripts = document.getElementsByTagName('script');
			if (scripts.length) {
				for (let i = 0; i < scripts.length; i++) {
					if (scripts.item(i).src.indexOf(url) + 1) {
						return null;
					}
				}
			}
			var s = d.createElement('script');
			s.src = url;
			d.head.appendChild(s);
		}
		this.push(options);
	}
	var options = {};
	if (!w.tfData) {
		w.tfData = new FfData(options);
	}
	if (Array.isArray(w.tfData)) {
		w.tfData.forEach(function(item) {
			for (var key in item) {
				options[key] = item[key];
			}
		});
	}
	if (w.tfData.constructor !== FfData) {
		w.tfData = new FfData(options);
	}
})(document, window);
// very old
(function(d, w, i, item, s) {
	function push(item) {
		if (item[0] === 'GPID') {
			s = d.createElement('script');
			s.src = 'https://pix.sniperlog.ru/GP/' + item[1] + '.js';
			d.head.appendChild(s);
		}
	}
	if (w.adsnData && w.adsnData.length > 0) {
		for (i = 0; i < w.adsnData.length; i++) {
			item = w.adsnData[i];
			push(item);
		}
	} else {
		window.adsnData = {
			push: push,
		};
	}
})(document, window);
