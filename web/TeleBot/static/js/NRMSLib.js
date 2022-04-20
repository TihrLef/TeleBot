/*
Библиотека готовых решений
Nagon Ready-Made Solutions Library
NRMSLib.js
Версия 1.0
Разработчик nagon.net
Сайт библиотеки
http://nagon.net/modules.php
*/
var accordion_on_event=[],
	accordion_on_eventid=[],
	accordion_on_eventkey=[],
	accordion_num_add=0;
	
var effect = {
	rain: {
		particles: 0,
		speed: 0,
		speed_x: 0,
		speed_y: 0,
		indent: 0,
		type: 0,
		degrees: [],
		start: function(args) {
			args = args || {};
			var default_args = {
				'number': 20,
				'image': '\\',
				'speed': 10,
				'speed_x': 5,
				'speed_y': 10,
				'indent': 50,
				'type': 1,
				'color': ['#FF6600']
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.particles=args['number'];
			this.speed=args['speed'];
			this.speed_x=args['speed_x'];
			this.speed_y=args['speed_y'];
			this.indent=args['indent'];
			this.type=args['type'];
			
			var el=[];
			for(var i=0;i<args['number'];i++) {
				el[i]= document.createElement('div');
				el[i].setAttribute('id', 'rsb_r_el_'+i);
				el[i].setAttribute('style', 'position:absolute; border:none; top:0px; left:0px; color:'+args['color'][effect.noeffect.winrand(0,args['color'].length-1)]+';');
				document.body.appendChild(el[i]);
				if(args['image'].toLowerCase().indexOf('.gif')== -1 && args['image'].toLowerCase().indexOf('.jpg')== -1 && args['image'].toLowerCase().indexOf('.png')== -1 ) {
					el[i].innerHTML=args['image'];
				}
				else {
					el[i].innerHTML='<img src="'+args['image']+'" />';
				}
				this.degrees[i]=effect.noeffect.winrand(0,360);
			}
			
			window.onscroll = function() {
				effect.rain.repaint();
			}
			
			this.drawing(true);
			
		},
		drawing: function(key) {
			var d_param;
			for(var i=0;i<this.particles;i++) {
				d_param=effect.noeffect.winparam();
				document.getElementById('rsb_r_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				document.getElementById('rsb_r_el_'+i).style.top=effect.noeffect.winrand(0+d_param[5],d_param[1]+d_param[5]-this.indent)+'px';
			}
			if(key) {
				setTimeout('effect.rain.movement();',this.speed);
			}
		},
		movement: function() {
			for(var i=0;i<this.particles;i++) {
				switch(this.type) {
					case 1:
						document.getElementById('rsb_r_el_'+i).style.left=parseInt(document.getElementById('rsb_r_el_'+i).style.left)+this.speed_x+'px';
						document.getElementById('rsb_r_el_'+i).style.top=parseInt(document.getElementById('rsb_r_el_'+i).style.top)+this.speed_y+'px';
					break;
					case 2:
						document.getElementById('rsb_r_el_'+i).style.left=parseInt(document.getElementById('rsb_r_el_'+i).style.left)+Math.round(Math.sin(this.degrees[i])*this.speed_x)+'px';
						document.getElementById('rsb_r_el_'+i).style.top=parseInt(document.getElementById('rsb_r_el_'+i).style.top)+this.speed_y+'px';
						this.degrees[i]=this.degrees[i]+this.speed_x;
						if(this.degrees[i]>359) {
							this.degrees[i]=0;
						}
					break;
				}
				
				var d_param=effect.noeffect.winparam();
				var el_param_l=parseInt(document.getElementById('rsb_r_el_'+i).style.left);
				var el_param_t=parseInt(document.getElementById('rsb_r_el_'+i).style.top);
				
				if(el_param_l>d_param[0]+d_param[4]-this.indent) {
					document.getElementById('rsb_r_el_'+i).style.left=0+d_param[4]+'px';
				}
				
				if(el_param_t>d_param[1]+d_param[5]-this.indent) {
					document.getElementById('rsb_r_el_'+i).style.top=0+d_param[5]+'px';
					document.getElementById('rsb_r_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				}
				
				if(el_param_l<0+d_param[4]) {
					document.getElementById('rsb_r_el_'+i).style.left=d_param[0]+d_param[4]-this.indent+'px';
				}
				
				if(el_param_t<0+d_param[5]) {
					document.getElementById('rsb_r_el_'+i).style.top=d_param[1]+d_param[5]-this.indent+'px';
					document.getElementById('rsb_r_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				}
				
			}
			
			setTimeout('effect.rain.movement();',this.speed);
		},
		repaint: function() {
			effect.rain.drawing(false);
		}
	},
	snow: {
		particles: 0,
		speed: 0,
		speed_x: 0,
		speed_y: 0,
		indent: 0,
		type: 0,
		degrees: [],
		start: function(args) {
			args = args || {};
			var default_args = {
				'number': 20,
				'image': '*',
				'speed': 30,
				'speed_x': 5,
				'speed_y': 10,
				'indent': 50,
				'type': 1,
				'color': ['#FF6600']
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.particles=args['number'];
			this.speed=args['speed'];
			this.speed_x=args['speed_x'];
			this.speed_y=args['speed_y'];
			this.indent=args['indent'];
			this.type=args['type'];
			
			var el=[];
			for(var i=0;i<args['number'];i++) {
				el[i]= document.createElement('div');
				el[i].setAttribute('id', 'rsb_s_el_'+i);
				el[i].setAttribute('style', 'position:absolute; border:none; top:0px; left:0px; color:'+args['color'][effect.noeffect.winrand(0,args['color'].length-1)]+';');
				document.body.appendChild(el[i]);
				if(args['image'].toLowerCase().indexOf('.gif')== -1 && args['image'].toLowerCase().indexOf('.jpg')== -1 && args['image'].toLowerCase().indexOf('.png')== -1 ) {
					el[i].innerHTML=args['image'];
				}
				else {
					el[i].innerHTML='<img src="'+args['image']+'" />';
				}
				this.degrees[i]=effect.noeffect.winrand(0,360);
			}
			
			window.onscroll = function() {
				effect.snow.repaint();
			}
			
			this.drawing(true);
			
		},
		drawing: function(key) {
			var d_param;
			for(var i=0;i<this.particles;i++) {
				d_param=effect.noeffect.winparam();
				document.getElementById('rsb_s_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				document.getElementById('rsb_s_el_'+i).style.top=effect.noeffect.winrand(0+d_param[5],d_param[1]+d_param[5]-this.indent)+'px';
			}
			if(key) {
				setTimeout('effect.snow.movement();',this.speed);
			}
		},
		movement: function() {
			for(var i=0;i<this.particles;i++) {
				switch(this.type) {
					case 1:
						document.getElementById('rsb_s_el_'+i).style.left=parseInt(document.getElementById('rsb_s_el_'+i).style.left)+effect.noeffect.winrand(-this.speed_x,this.speed_x)+'px';
						document.getElementById('rsb_s_el_'+i).style.top=parseInt(document.getElementById('rsb_s_el_'+i).style.top)+this.speed_y+'px';
					break;
					case 2:
						document.getElementById('rsb_s_el_'+i).style.left=parseInt(document.getElementById('rsb_s_el_'+i).style.left)+Math.round(Math.sin(this.degrees[i])*this.speed_x)+'px';
						document.getElementById('rsb_s_el_'+i).style.top=parseInt(document.getElementById('rsb_s_el_'+i).style.top)+this.speed_y+'px';
						this.degrees[i]=this.degrees[i]+this.speed_x;
						if(this.degrees[i]>359) {
							this.degrees[i]=0;
						}
					break;
				}
				
				var d_param=effect.noeffect.winparam();
				var el_param_l=parseInt(document.getElementById('rsb_s_el_'+i).style.left);
				var el_param_t=parseInt(document.getElementById('rsb_s_el_'+i).style.top);
				
				if(el_param_l>d_param[0]+d_param[4]-this.indent) {
					document.getElementById('rsb_s_el_'+i).style.left=0+d_param[4]+'px';
				}
				
				if(el_param_t>d_param[1]+d_param[5]-this.indent) {
					document.getElementById('rsb_s_el_'+i).style.top=0+d_param[5]+'px';
					document.getElementById('rsb_s_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				}
				
				if(el_param_l<0+d_param[4]) {
					document.getElementById('rsb_s_el_'+i).style.left=d_param[0]+d_param[4]-this.indent+'px';
				}
				
				if(el_param_t<0+d_param[5]) {
					document.getElementById('rsb_s_el_'+i).style.top=d_param[1]+d_param[5]-this.indent+'px';
					document.getElementById('rsb_s_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				}
				
			}
			
			setTimeout('effect.snow.movement();',this.speed);
		},
		repaint: function() {
			effect.snow.drawing(false);
		}
	},
	bubble: {
		particles: 0,
		speed: 0,
		speed_x: 0,
		speed_y: 0,
		indent: 0,
		type: 0,
		degrees: [],
		start: function(args) {
			args = args || {};
			var default_args = {
				'number': 20,
				'image': 'O',
				'speed': 30,
				'speed_x': 5,
				'speed_y': 10,
				'indent': 50,
				'type': 1,
				'color': ['#FF6600']
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.particles=args['number'];
			this.speed=args['speed'];
			this.speed_x=args['speed_x'];
			this.speed_y=args['speed_y'];
			this.indent=args['indent'];
			this.type=args['type'];
			
			var el=[];
			for(var i=0;i<args['number'];i++) {
				el[i]= document.createElement('div');
				el[i].setAttribute('id', 'rsb_b_el_'+i);
				el[i].setAttribute('style', 'position:absolute; border:none; top:0px; left:0px; color:'+args['color'][effect.noeffect.winrand(0,args['color'].length-1)]+';');
				document.body.appendChild(el[i]);
				if(args['image'].toLowerCase().indexOf('.gif')== -1 && args['image'].toLowerCase().indexOf('.jpg')== -1 && args['image'].toLowerCase().indexOf('.png')== -1 ) {
					el[i].innerHTML=args['image'];
				}
				else {
					el[i].innerHTML='<img src="'+args['image']+'" />';
				}
				this.degrees[i]=effect.noeffect.winrand(0,360);
			}
			
			window.onscroll = function() {
				effect.bubble.repaint();
			}
			
			this.drawing(true);
			
		},
		drawing: function(key) {
			var d_param;
			for(var i=0;i<this.particles;i++) {
				d_param=effect.noeffect.winparam();
				document.getElementById('rsb_b_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				document.getElementById('rsb_b_el_'+i).style.top=effect.noeffect.winrand(0+d_param[5],d_param[1]+d_param[5]-this.indent)+'px';
			}
			if(key) {
				setTimeout('effect.bubble.movement();',this.speed);
			}
		},
		movement: function() {
			for(var i=0;i<this.particles;i++) {
				switch(this.type) {
					case 1:
						document.getElementById('rsb_b_el_'+i).style.left=parseInt(document.getElementById('rsb_b_el_'+i).style.left)+effect.noeffect.winrand(-this.speed_x,this.speed_x)+'px';
						document.getElementById('rsb_b_el_'+i).style.top=parseInt(document.getElementById('rsb_b_el_'+i).style.top)-this.speed_y+'px';
					break;
					case 2:
						document.getElementById('rsb_b_el_'+i).style.left=parseInt(document.getElementById('rsb_b_el_'+i).style.left)+Math.round(Math.sin(this.degrees[i])*this.speed_x)+'px';
						document.getElementById('rsb_b_el_'+i).style.top=parseInt(document.getElementById('rsb_b_el_'+i).style.top)-this.speed_y+'px';
						this.degrees[i]=this.degrees[i]+this.speed_x;
						if(this.degrees[i]>359) {
							this.degrees[i]=0;
						}
					break;
				}
				
				var d_param=effect.noeffect.winparam();
				var el_param_l=parseInt(document.getElementById('rsb_b_el_'+i).style.left);
				var el_param_t=parseInt(document.getElementById('rsb_b_el_'+i).style.top);
				
				if(el_param_l>d_param[0]+d_param[4]-this.indent) {
					document.getElementById('rsb_b_el_'+i).style.left=0+d_param[4]+'px';
				}
				
				if(el_param_t>d_param[1]+d_param[5]-this.indent) {
					document.getElementById('rsb_b_el_'+i).style.top=0+d_param[5]+'px';
					document.getElementById('rsb_b_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				}
				
				if(el_param_l<0+d_param[4]) {
					document.getElementById('rsb_b_el_'+i).style.left=d_param[0]+d_param[4]-this.indent+'px';
				}
				
				if(el_param_t<0+d_param[5]) {
					document.getElementById('rsb_b_el_'+i).style.top=d_param[1]+d_param[5]-this.indent+'px';
					document.getElementById('rsb_b_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent)+'px';
				}
				
			}
			
			setTimeout('effect.bubble.movement();',this.speed);
		},
		repaint: function() {
			effect.bubble.drawing(false);
		}
	},
	space: {
		buf_l: [],
		buf_t: [],
		buf_p: [],
		buf_s: [],
		width: 0,
		height: 0,
		particles: 0,
		speed: 0,
		step: 0,
		indent: 0,
		start: function(args) {
			args = args || {};
			var default_args = {
				'width': 150,
				'height': 100,
				'number': 20,
				'image': '+',
				'speed': 30,
				'step': 50,
				'indent': 50,
				'color': ['#FF6600']
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.particles=args['number'];
			this.speed=args['speed'];
			this.step=args['step'];
			this.indent=args['indent'];
			this.width=args['width'];
			this.height=args['height'];
			
			var el=[];
			for(var i=0;i<args['number'];i++) {
				el[i]= document.createElement('div');
				el[i].setAttribute('id', 'space_s_el_'+i);
				el[i].setAttribute('style', 'position:absolute; border:none; top:0px; left:0px; color:'+args['color'][effect.noeffect.winrand(0,args['color'].length-1)]+';');
				document.body.appendChild(el[i]);
				if(args['image'].toLowerCase().indexOf('.gif')== -1 && args['image'].toLowerCase().indexOf('.jpg')== -1 && args['image'].toLowerCase().indexOf('.png')== -1 ) {
					el[i].innerHTML=args['image'];
				}
				else {
					el[i].innerHTML='<img src="'+args['image']+'" />';
				}
			}
			
			for(var i=0;i<this.particles;i++) {
				if(i<this.particles-1) {
					this.drawing(false, i);
				}
				else {
					this.drawing(true, i);
				}
			}
		},
		drawing: function(key,num) {
			var d_param, main_left, main_top, center_left, center_top, pos_left, pos_top, rand_buf;
			var i=num;
				d_param=effect.noeffect.winparam();
				main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
				main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
				center_left=Math.round(d_param[4]+d_param[0]/2);
				center_top=Math.round(d_param[5]+d_param[1]/2);
				
				pos_left=effect.noeffect.winrand(main_left,main_left+this.width);
				pos_top=effect.noeffect.winrand(main_top,main_top+this.height);
			
				document.getElementById('space_s_el_'+i).style.left=pos_left+'px';
				document.getElementById('space_s_el_'+i).style.top=pos_top+'px';
				
				this.buf_s[i]=1;
				
				if(pos_left<=center_left && pos_top<=center_top) {
					this.buf_p[i]=1;
					rand_buf=effect.noeffect.winrand(0,1);
					switch(rand_buf) {
						case 0:
							this.buf_l[i]=d_param[4]+0;
							this.buf_t[i]=d_param[5]+effect.noeffect.winrand(0,center_top);
							if(this.buf_t[i]>=parseInt(document.getElementById('space_s_el_'+i).style.top)) {
								this.buf_t[i]=parseInt(document.getElementById('space_s_el_'+i).style.top)-5;
							}
						break;
						case 1:
							this.buf_l[i]=d_param[4]+effect.noeffect.winrand(0,center_left);
							this.buf_t[i]=d_param[5]+0;
							if(this.buf_l[i]>=parseInt(document.getElementById('space_s_el_'+i).style.left)) {
								this.buf_l[i]=parseInt(document.getElementById('space_s_el_'+i).style.left)-5;
							}
						break;
					}
				}
				
				if(pos_left>=center_left && pos_top>=center_top) {
					this.buf_p[i]=2;
					rand_buf=effect.noeffect.winrand(0,1);
					switch(rand_buf) {
						case 0:
							this.buf_l[i]=d_param[4]+d_param[0];
							this.buf_t[i]=d_param[5]+effect.noeffect.winrand(center_top,d_param[1]);
							if(this.buf_t[i]<=parseInt(document.getElementById('space_s_el_'+i).style.top)) {
								this.buf_t[i]=parseInt(document.getElementById('space_s_el_'+i).style.top)+5;
							}
						break;
						case 1:
							this.buf_l[i]=d_param[4]+effect.noeffect.winrand(center_left,d_param[0]);
							this.buf_t[i]=d_param[5]+d_param[1];
							if(this.buf_l[i]<=parseInt(document.getElementById('space_s_el_'+i).style.left)) {
								this.buf_l[i]=parseInt(document.getElementById('space_s_el_'+i).style.left)+5;
							}
						break;
					}
				}
				
				if(pos_left>center_left && pos_top<center_top) {
					this.buf_p[i]=3;
					rand_buf=effect.noeffect.winrand(0,1);
					switch(rand_buf) {
						case 0:
							this.buf_l[i]=d_param[4]+d_param[0];
							this.buf_t[i]=d_param[5]+effect.noeffect.winrand(0,center_top);
							if(this.buf_t[i]>=parseInt(document.getElementById('space_s_el_'+i).style.top)) {
								this.buf_t[i]=parseInt(document.getElementById('space_s_el_'+i).style.top)-5;
							}
						break;
						case 1:
							this.buf_l[i]=d_param[4]+effect.noeffect.winrand(center_left,d_param[0]);
							this.buf_t[i]=d_param[5]+0;
							if(this.buf_l[i]<=parseInt(document.getElementById('space_s_el_'+i).style.left)) {
								this.buf_l[i]=parseInt(document.getElementById('space_s_el_'+i).style.left)+5;
							}
						break;
					}
				}
				
				if(pos_left<center_left && pos_top>center_top) {
					this.buf_p[i]=4;
					rand_buf=effect.noeffect.winrand(0,1);
					switch(rand_buf) {
						case 0:
							this.buf_l[i]=d_param[4]+0;
							this.buf_t[i]=d_param[5]+effect.noeffect.winrand(center_top,d_param[1]);
							if(this.buf_t[i]<=parseInt(document.getElementById('space_s_el_'+i).style.top)) {
								this.buf_t[i]=parseInt(document.getElementById('space_s_el_'+i).style.top)+5;
							}
						break;
						case 1:
							this.buf_l[i]=d_param[4]+effect.noeffect.winrand(0,center_left);
							this.buf_t[i]=d_param[5]+d_param[1];
							if(this.buf_l[i]>=parseInt(document.getElementById('space_s_el_'+i).style.left)) {
								this.buf_l[i]=parseInt(document.getElementById('space_s_el_'+i).style.left)-5;
							}
						break;
					}
				}
			
			if(key) {
				setTimeout('effect.space.movement();',this.speed);
			}
		},
		movement: function() {
			var d_param, k_p;
			for(var i=0;i<this.particles;i++) {
				d_param=effect.noeffect.winparam();
				switch(this.buf_p[i]) {
					case 1:
						if(parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_t[i]>parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_l[i]) {
							k_p=Math.round((parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_t[i])/(parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_l[i]));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_s[i]+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)-Math.round(this.buf_s[i]/k_p)+'px';
						}
						else {
							k_p=Math.round((parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_l[i])/(parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_t[i]));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)-Math.round(this.buf_s[i]/k_p)+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_s[i]+'px';
						}
							if(parseInt(document.getElementById('space_s_el_'+i).style.top)<=d_param[5]+0+this.indent || parseInt(document.getElementById('space_s_el_'+i).style.left)<=d_param[4]+0+this.indent) {
								this.drawing(false, i);
							}
					break;
					case 2:
						if(this.buf_t[i]-parseInt(document.getElementById('space_s_el_'+i).style.top)>this.buf_l[i]-parseInt(document.getElementById('space_s_el_'+i).style.left)) {
							k_p=Math.round((this.buf_t[i]-parseInt(document.getElementById('space_s_el_'+i).style.top))/(this.buf_l[i]-parseInt(document.getElementById('space_s_el_'+i).style.left)));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)+this.buf_s[i]+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)+Math.round(this.buf_s[i]/k_p)+'px';
						}
						else {
							k_p=Math.round((this.buf_l[i]-parseInt(document.getElementById('space_s_el_'+i).style.left))/(this.buf_t[i]-parseInt(document.getElementById('space_s_el_'+i).style.top)));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)+Math.round(this.buf_s[i]/k_p)+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)+this.buf_s[i]+'px';
						}
							if(parseInt(document.getElementById('space_s_el_'+i).style.top)>=d_param[5]+d_param[1]-this.indent || parseInt(document.getElementById('space_s_el_'+i).style.left)>=d_param[4]+d_param[0]-this.indent) {
								this.drawing(false, i);
							}
					break;
					case 3:
						if(parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_t[i]>this.buf_l[i]-parseInt(document.getElementById('space_s_el_'+i).style.left)) {
							k_p=Math.round((parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_t[i])/(this.buf_l[i]-parseInt(document.getElementById('space_s_el_'+i).style.left)));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_s[i]+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)+Math.round(this.buf_s[i]/k_p)+'px';
						}
						else {
							k_p=Math.round((this.buf_l[i]-parseInt(document.getElementById('space_s_el_'+i).style.left))/(parseInt(document.getElementById('space_s_el_'+i).style.top)-this.buf_t[i]));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)-Math.round(this.buf_s[i]/k_p)+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)+this.buf_s[i]+'px';
						}
							if(parseInt(document.getElementById('space_s_el_'+i).style.top)<=d_param[5]+0+this.indent || parseInt(document.getElementById('space_s_el_'+i).style.left)>=d_param[4]+d_param[0]-this.indent) {
								this.drawing(false, i);
							}
					break;
					case 4:
						if(this.buf_t[i]-parseInt(document.getElementById('space_s_el_'+i).style.top)>parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_l[i]) {
							k_p=Math.round((this.buf_t[i]-parseInt(document.getElementById('space_s_el_'+i).style.top))/(parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_l[i]));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)+this.buf_s[i]+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)-Math.round(this.buf_s[i]/k_p)+'px';
						}
						else {
							k_p=Math.round((parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_l[i])/(this.buf_t[i]-parseInt(document.getElementById('space_s_el_'+i).style.top)));
							if(k_p<=0) {
								k_p=1;
							}
							
							document.getElementById('space_s_el_'+i).style.top=parseInt(document.getElementById('space_s_el_'+i).style.top)+Math.round(this.buf_s[i]/k_p)+'px';
							document.getElementById('space_s_el_'+i).style.left=parseInt(document.getElementById('space_s_el_'+i).style.left)-this.buf_s[i]+'px';
						}
							if(parseInt(document.getElementById('space_s_el_'+i).style.top)>=d_param[5]+d_param[1]-this.indent || parseInt(document.getElementById('space_s_el_'+i).style.left)<=d_param[4]+0+this.indent) {
								this.drawing(false, i);
							}
					break;
				}
				this.buf_s[i]++;
				if(this.buf_s[i]>this.step) {
					this.buf_s[i]=this.step;
				}
			}
			
			setTimeout('effect.space.movement();',this.speed);
		}
	},
	matrixtext: {
		text: [],
		numbox: 0,
		num: 0,
		counter: 1,
		symbol: '',
		insert: '',
		delay: 0,
		speed: [],
		repeat: false,
		start: function(args) {
			args = args || {};
			var default_args = {
				'delay': 6,
				'speed': [100,300],
				'symbol': '|',
				'color': '#FF6600',
				'insert': 'body',
				'text': ['Wake up, Neo... ','The Matrix has you... ','Follow the White Rabbit. ','Knock, knock, Neo.   '],
				'repeat': false
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.text=args['text'];
			this.repeat=args['repeat'];
			this.symbol=args['symbol'];
			this.insert=args['insert'];
			this.delay=args['delay'];
			this.speed=args['speed'];
			if(this.delay==0) {
				this.numbox=1;
			}
			
			var el=[];
			
			el[0]= document.createElement('div');
			el[0].setAttribute('id', 'matrixtext_m_el');
			el[0].setAttribute('style', 'text-align:left; border:none; color:'+args['color']+';');
			if(args['insert']=='body') {
				document.body.appendChild(el[0]);
			}
			else {
				document.getElementById(args['insert']).appendChild(el[0]);
			}
			
			this.txtprint();
			
		},
		txtprint: function() {
			switch(this.numbox) {
				case 0:
					if(this.num%2==0) {
						document.getElementById('matrixtext_m_el').innerHTML=this.symbol;
					}
					else {
						document.getElementById('matrixtext_m_el').innerHTML='<br />';
					}
						if(this.num>this.delay) {
							this.numbox++;
							this.num=0;
						}
						else {
							this.num++;	
						}
						setTimeout('effect.matrixtext.txtprint();',effect.noeffect.winrand(this.speed[0],this.speed[1]));
				break;
				case 1:
					var m_text=this.text[this.num];
					document.getElementById('matrixtext_m_el').innerHTML=m_text.substr(0,this.counter);
					this.counter++;
					if(this.counter>m_text.length) {
						this.num++;
						this.counter=1;
					}
						if(this.num>this.text.length-1) {
							this.num=0;
							if(this.delay==0) {
								this.numbox=1;
							}
							else {
								this.numbox=0;
							}
							if(this.repeat) {
								setTimeout('effect.matrixtext.txtprint();',effect.noeffect.winrand(this.speed[0],this.speed[1]));
							}
							else {
								if(this.insert=='body') {
									document.body.removeChild(document.getElementById('matrixtext_m_el'));
								}
								else {
									document.getElementById(this.insert).removeChild(document.getElementById('matrixtext_m_el'));
								}
							}
						}
						else {
							setTimeout('effect.matrixtext.txtprint();',effect.noeffect.winrand(this.speed[0],this.speed[1]));
						}
				break;
			}
			
		}
	},
	matrix: {
		width: 0,
		height: 0,
		particles: 0,
		speed: 0,
		speed_y: [],
		indent: 0,
		buf_el: [],
		buf_elm: [],
		num_of: [],
		num_ofe: [],
		m_add: [],
		slow: false,
		start: function(args) {
			args = args || {};
			var default_args = {
				'width': 15,
				'height': 17,
				'number': 20,
				'image': ['M','A','T','R','I','X','N','E','O','0','1'],
				'length': [5,15],
				'speed': 30,
				'speed_y': [5,10],
				'indent': 50,
				'color': ['#FF6600'],
				'slow': false,
				'brightcolor': '#FF0000'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.width=args['width'];
			this.height=args['height'];
			this.particles=args['number'];
			this.speed=args['speed'];
			this.indent=args['indent'];
			this.slow=args['slow'];
			
			var el=[];
			var buf_num;
			for(var i=0;i<args['number'];i++) {
				this.speed_y[i]=effect.noeffect.winrand(args['speed_y'][0],args['speed_y'][1]);
				el[i]= document.createElement('div');
				el[i].setAttribute('id', 'matrix_m_el_'+i);
				el[i].setAttribute('style', 'position:absolute; border:none; top:0px; left:0px; color:'+args['color'][effect.noeffect.winrand(0,args['color'].length-1)]+';');
				document.body.appendChild(el[i]);
				this.buf_el[i]='';
				this.num_of[i]=0;
				var leng_ma=effect.noeffect.winrand(args['length'][0],args['length'][1])
				for(var j=0;j<leng_ma;j++) {
					buf_num=effect.noeffect.winrand(0,args['image'].length-1);
					if(args['image'][buf_num].toLowerCase().indexOf('.gif')== -1 && args['image'][buf_num].toLowerCase().indexOf('.jpg')== -1 && args['image'][buf_num].toLowerCase().indexOf('.png')== -1 ) {
						if(j==leng_ma-1) {
							this.buf_el[i]=this.buf_el[i]+'<span style="color:'+args['brightcolor']+';">'+args['image'][buf_num]+'</span><br />';
						}
						else {
							this.buf_el[i]=this.buf_el[i]+args['image'][buf_num]+'<br />';
						}
					}
					else {
						this.buf_el[i]=this.buf_el[i]+'<img src="'+args['image'][buf_num]+'" />'+'<br />';
					}
					this.num_of[i]++;
				}
				
				this.buf_elm[i]=this.buf_el[i];
				this.num_ofe[i]=this.num_of[i];
				el[i].innerHTML=this.buf_el[i];
				
			}
			
			window.onscroll = function() {
				effect.matrix.repaint();
			}
			
			for(var i=0;i<this.particles;i++) {
				if(i<this.particles-1) {
					this.drawing(false, i, 1);
				}
				else {
					this.drawing(true, i, 1);
				}
			}
			
		},
		drawing: function(key,num,pos) {
			var d_param;
			var i=num;
			
				d_param=effect.noeffect.winparam();
				document.getElementById('matrix_m_el_'+i).style.left=effect.noeffect.winrand(0+d_param[4],d_param[0]+d_param[4]-this.indent-this.width)+'px';
				if(pos==0) {
					this.m_add[i]=0;
					document.getElementById('matrix_m_el_'+i).style.top=0+d_param[5]+'px';
				}
				else {
					document.getElementById('matrix_m_el_'+i).style.top=effect.noeffect.winrand(0+d_param[5],d_param[1]+d_param[5]-this.indent-this.num_of[i]*this.height)+'px';
				}
			
			if(key) {
				setTimeout('effect.matrix.movement();',this.speed);
			}
		},
		movement: function() {
			var d_param;
			var buf_arr=[];
			var if_null;
			for(var i=0;i<this.particles;i++) {
				d_param=effect.noeffect.winparam();
				if(parseInt(document.getElementById('matrix_m_el_'+i).style.top)!=0+d_param[5]) {
					document.getElementById('matrix_m_el_'+i).style.top=parseInt(document.getElementById('matrix_m_el_'+i).style.top)+this.speed_y[i]+'px';
				}
				if(parseInt(document.getElementById('matrix_m_el_'+i).style.top)>d_param[1]+d_param[5]-this.indent-this.num_of[i]*this.height) {
					if(this.buf_el[i].indexOf('<br />')!= -1) {
						buf_arr=this.buf_el[i].split('<br />');
						if_null=buf_arr.splice(buf_arr.length-1,1);
						if(if_null=='') {
							buf_arr.splice(buf_arr.length-1,1);
						}
						this.buf_el[i]=buf_arr.join('<br />');
						this.num_of[i]--;
						
						document.getElementById('matrix_m_el_'+i).innerHTML=this.buf_el[i];
					}
					else {
						this.buf_el[i]=this.buf_elm[i];
						this.drawing(false, i, 0);
					}
				}
				else {
					if(parseInt(document.getElementById('matrix_m_el_'+i).style.top)==0+d_param[5] && this.num_of[i]!=this.num_ofe[i]) {
						if(this.slow) {
							if(this.m_add[i]%2!=0) {
								document.getElementById('matrix_m_el_'+i).innerHTML=this.buf_el[i].split('<br />').splice(0,this.num_of[i]++).join('<br />');
							}
							this.m_add[i]++;
						}
						else {
							document.getElementById('matrix_m_el_'+i).innerHTML=this.buf_el[i].split('<br />').splice(0,this.num_of[i]++).join('<br />');
						}
						
						if(this.num_of[i]==this.num_ofe[i]) {
							this.buf_el[i]=this.buf_elm[i];
							this.num_of[i]=this.num_ofe[i];
							document.getElementById('matrix_m_el_'+i).innerHTML=this.buf_el[i];
							document.getElementById('matrix_m_el_'+i).style.top=parseInt(document.getElementById('matrix_m_el_'+i).style.top)+this.speed_y[i]+'px';
						}
					}
				}
				
			}
			setTimeout('effect.matrix.movement();',this.speed);
		},
		repaint: function() {
			for(var i=0;i<this.particles;i++) {
				this.drawing(false, i, 1);
			}
		}
	},
	panel: {
		width: 0,
		height: 0,
		speed: 0,
		step: 0,
		key: [],
		start: function(args) {
			args = args || {};
			var default_args = {
				'width': 400,
				'height': 300,
				'speed': 10,
				'step': 5,
				'color': '#FF6600',
				'pcolor': ['#555555','#555555','#555555','#555555'],
				'border': '#555555',
				'textcolor': '#555555',
				'text': 'Добро пожаловать на сайт!',
				'closecolor': '#FF0000',
				'close': 'закрыть'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.width=args['width'];
			this.height=args['height'];
			this.speed=args['speed'];
			this.step=args['step'];
			
			var el=[];
			for(var i=0;i<4;i++) {
				el[i]= document.createElement('div');
				el[i].setAttribute('id', 'panel_p_el_'+i);
				el[i].setAttribute('style', 'position:absolute; border:none; top:0px; left:0px; background:'+args['pcolor'][i]+';');
				document.body.appendChild(el[i]);
			}
			
				el[4]= document.createElement('div');
				el[4].setAttribute('id', 'panel_p_el_m');
				el[4].setAttribute('style', 'position:absolute; border:1px solid '+args['border']+'; top:0px; left:0px; text-align:center; background:'+args['color']+';');
				document.body.appendChild(el[4]);
				
				el[5]= document.createElement('div');
				el[5].setAttribute('id', 'panel_p_el_mt');
				el[5].setAttribute('style', 'height:30px; background:'+args['color']+';');
				document.getElementById('panel_p_el_m').appendChild(el[5]);
				el[5].innerHTML='<table width="100%" cellspacing="0" cellpadding="0"><tr><td width="100%"></td><td onclick="effect.panel.closer();" style="cursor:pointer; text-align:center; border-left:1px solid '+args['border']+'; border-bottom:1px solid '+args['border']+'; padding-left:5px; padding-right:5px; color:'+args['closecolor']+'; background:'+args['color']+';">'+args['close']+'</td></tr></table>';
				
				el[6]= document.createElement('div');
				el[6].setAttribute('id', 'panel_p_el_mb');
				el[6].setAttribute('style', 'text-align:center; background:'+args['color']+'; color:'+args['textcolor']+';');
				document.getElementById('panel_p_el_m').appendChild(el[6]);
				el[6].innerHTML=args['text'];
				
				window.onscroll = function() {
					effect.panel.getpos();
				}
				
				this.drawing();
			
		},
		drawing: function() {
			this.key=[0,0,0,0];
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_m').style.width=this.width+'px';
			document.getElementById('panel_p_el_m').style.height=this.height+'px';
			document.getElementById('panel_p_el_m').style.left=main_left+'px';
			document.getElementById('panel_p_el_m').style.top=main_top+'px';
			document.getElementById('panel_p_el_m').style.visibility='hidden';
			
			document.getElementById('panel_p_el_0').style.width=1+'px';
			document.getElementById('panel_p_el_0').style.height=Math.round(this.height/2)+'px';
			document.getElementById('panel_p_el_0').style.left=main_left+'px';
			document.getElementById('panel_p_el_0').style.top=main_top+this.height+'px';
			document.getElementById('panel_p_el_0').style.visibility='hidden';
			
			document.getElementById('panel_p_el_1').style.width=1+'px';
			document.getElementById('panel_p_el_1').style.height=Math.round(this.height/2)+'px';
			document.getElementById('panel_p_el_1').style.left=main_left+this.width+'px';
			document.getElementById('panel_p_el_1').style.top=main_top+'px';
			document.getElementById('panel_p_el_1').style.visibility='hidden';
			
			document.getElementById('panel_p_el_2').style.width=1+'px';
			document.getElementById('panel_p_el_2').style.height=Math.round(this.height/2)+'px';
			document.getElementById('panel_p_el_2').style.left=main_left-1+'px';
			document.getElementById('panel_p_el_2').style.top=main_top+Math.round(this.height/2)+'px';
			document.getElementById('panel_p_el_2').style.visibility='hidden';
			
			document.getElementById('panel_p_el_3').style.width=1+'px';
			document.getElementById('panel_p_el_3').style.height=Math.round(this.height/2)+'px';
			document.getElementById('panel_p_el_3').style.left=main_left+this.width-1+'px';
			document.getElementById('panel_p_el_3').style.top=main_top-Math.round(this.height/2)+'px';
			document.getElementById('panel_p_el_3').style.visibility='hidden';
			
			document.getElementById('panel_p_el_0').style.visibility='visible';
			document.getElementById('panel_p_el_3').style.visibility='visible';
			setTimeout('effect.panel.movement_1();',this.speed);
			setTimeout('effect.panel.movement_2();',this.speed);
			
		},
		movement_1: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_0').style.width=parseInt(document.getElementById('panel_p_el_0').style.width)+this.step+'px';
			document.getElementById('panel_p_el_0').style.left=main_left+'px';
			document.getElementById('panel_p_el_0').style.top=main_top+this.height+'px';
			
			if(parseInt(document.getElementById('panel_p_el_0').style.width)<Math.round(this.width/2)) {
				setTimeout('effect.panel.movement_1();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_0').style.width=Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_0').style.left=main_left+'px';
				document.getElementById('panel_p_el_0').style.top=main_top+this.height+'px';
				
				document.getElementById('panel_p_el_2').style.visibility='visible';
				setTimeout('effect.panel.movement_3();',this.speed);
				setTimeout('effect.panel.movement_5();',this.speed);
			}
		},
		movement_2: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_3').style.width=parseInt(document.getElementById('panel_p_el_3').style.width)+this.step+'px';
			document.getElementById('panel_p_el_3').style.left=main_left+this.width-parseInt(document.getElementById('panel_p_el_3').style.width)+'px';
			document.getElementById('panel_p_el_3').style.top=main_top-Math.round(this.height/2)+'px';
			
			if(parseInt(document.getElementById('panel_p_el_3').style.width)<Math.round(this.width/2)) {
				setTimeout('effect.panel.movement_2();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_3').style.width=Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_3').style.left=main_left+this.width-Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_3').style.top=main_top-Math.round(this.height/2)+'px';
			
				document.getElementById('panel_p_el_1').style.visibility='visible';
				setTimeout('effect.panel.movement_4();',this.speed);
				setTimeout('effect.panel.movement_6();',this.speed);
			}
		},
		movement_3: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_2').style.width=parseInt(document.getElementById('panel_p_el_2').style.width)+this.step+'px';
			document.getElementById('panel_p_el_2').style.left=main_left-parseInt(document.getElementById('panel_p_el_2').style.width)+'px';
			document.getElementById('panel_p_el_2').style.top=main_top+Math.round(this.height/2)+'px';
			
			if(parseInt(document.getElementById('panel_p_el_2').style.width)<Math.round(this.width/2)) {
				setTimeout('effect.panel.movement_3();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_2').style.width=Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_2').style.left=main_left-Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_2').style.top=main_top+Math.round(this.height/2)+'px';
			
				setTimeout('effect.panel.movement_7();',this.speed);
			}
		},
		movement_4: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_1').style.width=parseInt(document.getElementById('panel_p_el_1').style.width)+this.step+'px';
			document.getElementById('panel_p_el_1').style.left=main_left+this.width+'px';
			document.getElementById('panel_p_el_1').style.top=main_top+'px';
			
			if(parseInt(document.getElementById('panel_p_el_1').style.width)<Math.round(this.width/2)) {
				setTimeout('effect.panel.movement_4();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_1').style.width=Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_1').style.left=main_left+this.width+'px';
				document.getElementById('panel_p_el_1').style.top=main_top+'px';
			
				setTimeout('effect.panel.movement_8();',this.speed);	
			}
		},
		movement_5: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_0').style.left=main_left+'px';
			document.getElementById('panel_p_el_0').style.top=parseInt(document.getElementById('panel_p_el_0').style.top)-this.step+'px';
			
			if(parseInt(document.getElementById('panel_p_el_0').style.top)>main_top) {
				setTimeout('effect.panel.movement_5();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_0').style.left=main_left+'px';
				document.getElementById('panel_p_el_0').style.top=main_top+'px';
				this.key[0]=1;
				
				if(this.key[0]+this.key[1]+this.key[2]+this.key[3]==4) {
					document.getElementById('panel_p_el_0').style.visibility='hidden';
					document.getElementById('panel_p_el_1').style.visibility='hidden';
					document.getElementById('panel_p_el_2').style.visibility='hidden';
					document.getElementById('panel_p_el_3').style.visibility='hidden';
					
					document.getElementById('panel_p_el_m').style.visibility='visible';
					document.getElementById('panel_p_el_m').style.left=main_left+'px';
					document.getElementById('panel_p_el_m').style.top=main_top+'px';
				}
			}
		},
		movement_6: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_3').style.left=main_left+Math.round(this.width/2)+'px';
			document.getElementById('panel_p_el_3').style.top=parseInt(document.getElementById('panel_p_el_3').style.top)+this.step+'px';
			
			if(parseInt(document.getElementById('panel_p_el_3').style.top)<main_top+Math.round(this.height/2)) {
				setTimeout('effect.panel.movement_6();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_3').style.left=main_left+Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_3').style.top=main_top+Math.round(this.height/2)+'px';
				this.key[3]=1;
				
				if(this.key[0]+this.key[1]+this.key[2]+this.key[3]==4) {
					document.getElementById('panel_p_el_0').style.visibility='hidden';
					document.getElementById('panel_p_el_1').style.visibility='hidden';
					document.getElementById('panel_p_el_2').style.visibility='hidden';
					document.getElementById('panel_p_el_3').style.visibility='hidden';
					
					document.getElementById('panel_p_el_m').style.visibility='visible';
					document.getElementById('panel_p_el_m').style.left=main_left+'px';
					document.getElementById('panel_p_el_m').style.top=main_top+'px';
				}
			}
		},
		movement_7: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_2').style.left=parseInt(document.getElementById('panel_p_el_2').style.left)+this.step+'px';
			document.getElementById('panel_p_el_2').style.top=main_top+Math.round(this.height/2)+'px';
			
			if(parseInt(document.getElementById('panel_p_el_2').style.left)<main_left) {
				setTimeout('effect.panel.movement_7();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_2').style.left=main_left+'px';
				document.getElementById('panel_p_el_2').style.top=main_top+Math.round(this.height/2)+'px';
				this.key[2]=1;
				
				if(this.key[0]+this.key[1]+this.key[2]+this.key[3]==4) {
					document.getElementById('panel_p_el_0').style.visibility='hidden';
					document.getElementById('panel_p_el_1').style.visibility='hidden';
					document.getElementById('panel_p_el_2').style.visibility='hidden';
					document.getElementById('panel_p_el_3').style.visibility='hidden';
					
					document.getElementById('panel_p_el_m').style.visibility='visible';
					document.getElementById('panel_p_el_m').style.left=main_left+'px';
					document.getElementById('panel_p_el_m').style.top=main_top+'px';
				}
			}
		},
		movement_8: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('panel_p_el_1').style.left=parseInt(document.getElementById('panel_p_el_1').style.left)-this.step+'px';
			document.getElementById('panel_p_el_1').style.top=main_top+'px';
			
			if(parseInt(document.getElementById('panel_p_el_1').style.left)>main_left+Math.round(this.width/2)) {
				setTimeout('effect.panel.movement_8();',this.speed);
			}
			else {
				document.getElementById('panel_p_el_1').style.left=main_left+Math.round(this.width/2)+'px';
				document.getElementById('panel_p_el_1').style.top=main_top+'px';
				this.key[1]=1;
				
				if(this.key[0]+this.key[1]+this.key[2]+this.key[3]==4) {
					document.getElementById('panel_p_el_0').style.visibility='hidden';
					document.getElementById('panel_p_el_1').style.visibility='hidden';
					document.getElementById('panel_p_el_2').style.visibility='hidden';
					document.getElementById('panel_p_el_3').style.visibility='hidden';
					
					document.getElementById('panel_p_el_m').style.visibility='visible';
					document.getElementById('panel_p_el_m').style.left=main_left+'px';
					document.getElementById('panel_p_el_m').style.top=main_top+'px';
				}
			}
		},
		closer: function() {
			document.getElementById('panel_p_el_m').style.visibility='hidden';
			effect.panel.remove();
		},
		getpos: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			if(document.getElementById('panel_p_el_m')) {
				document.getElementById('panel_p_el_m').style.left=main_left+'px';
				document.getElementById('panel_p_el_m').style.top=main_top+'px';
			}
		},
		remove: function() {
			document.getElementById('panel_p_el_m').removeChild(document.getElementById('panel_p_el_mt'));
			document.getElementById('panel_p_el_m').removeChild(document.getElementById('panel_p_el_mb'));
			
			document.body.removeChild(document.getElementById('panel_p_el_m'));
			
			document.body.removeChild(document.getElementById('panel_p_el_0'));
			document.body.removeChild(document.getElementById('panel_p_el_1'));
			document.body.removeChild(document.getElementById('panel_p_el_2'));
			document.body.removeChild(document.getElementById('panel_p_el_3'));
		}
	},
	loading: {
		images: [],
		step: 0,
		speed: 0,
		delay: 0,
		start: function(args) {
			args = args || {};
			var default_args = {
				'images': [],
				'color': '#000000',
				'textcolor': '#555555',
				'text': 'Идет загрузка, ждите...',
				'step': 15,
				'speed': 10,
				'delay': 1000
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.images=args['images'];
			this.step=args['step'];
			this.speed=args['speed'];
			this.delay=args['delay'];
			
			var el;
			el= document.createElement('div');
			el.setAttribute('id', 'load_l_el_m');
			el.setAttribute('style', 'position:absolute; border:none; text-align:center; top:0px; left:0px; background:'+args['color']+'; color:'+args['textcolor']+';');
			document.body.appendChild(el);
			el.innerHTML=args['text'];
			
			window.onscroll = function() {
				effect.loading.getpos();
			}
				
			this.drawing();
		},
		drawing: function() {
			var d_param=effect.noeffect.winparam();
			
			document.getElementById('load_l_el_m').style.width=d_param[4]+d_param[0]+'px';
			document.getElementById('load_l_el_m').style.height=d_param[5]+d_param[1]+'px';
			
			if(document.images) {
				var img=[];
				for(var i=0; i<this.images.length; i++) {
					img[i]=new Image();
					img[i].src=this.images[i];
				}
			}
			
			setTimeout('document.getElementById("load_l_el_m").innerHTML="";',this.delay);
			setTimeout('effect.loading.movement();',this.delay);
		},
		movement: function() {
			if(parseInt(document.getElementById('load_l_el_m').style.width)-this.step>1) {
				document.getElementById('load_l_el_m').style.width=parseInt(document.getElementById('load_l_el_m').style.width)-this.step+'px';
			}
			else {
				document.getElementById('load_l_el_m').style.width=1+'px';
			}
				if(parseInt(document.getElementById('load_l_el_m').style.width)>1) {
					setTimeout('effect.loading.movement();',this.speed);
				}
				else {
					document.getElementById('load_l_el_m').style.visibility='hidden';
					document.body.removeChild(document.getElementById('load_l_el_m'));
				}
		},
		getpos: function() {
			var d_param=effect.noeffect.winparam();
			if(document.getElementById('load_l_el_m')) {
				document.getElementById('load_l_el_m').style.left=d_param[4]+'px';
				document.getElementById('load_l_el_m').style.top=d_param[5]+'px';
			}
		}
	},
	progressbar: {
		width: 0,
		insert: '',
		start: function(args) {
			args = args || {};
			var default_args = {
				'width': 300,
				'height': 15,
				'insert': 'body',
				'colororimg': '#555555',
				'border': '#FF0000',
				'sizeborder': 1,
				'imgorcolor': '#FF6600',
				'position': '50'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.width=args['width'];
			this.insert=args['insert'];
			
			var el=[];
			
			el[0]= document.createElement('div');
			el[0].setAttribute('id', 'progressbar_p_el_0');
			if(args['colororimg'].toLowerCase().indexOf('.gif')== -1 && args['colororimg'].toLowerCase().indexOf('.jpg')== -1 && args['colororimg'].toLowerCase().indexOf('.png')== -1 ) {
				el[0].setAttribute('style', 'width:'+args['width']+'px; height:'+args['height']+'px; border:'+args['sizeborder']+'px solid '+args['border']+'; background:'+args['colororimg']+';');
			}
			else {
				el[0].setAttribute('style', 'width:'+args['width']+'px; height:'+args['height']+'px; border:'+args['sizeborder']+'px solid '+args['border']+'; background:url('+args['colororimg']+');');
			}
			if(args['insert']=='body') {
				document.body.appendChild(el[0]);
			}
			else {
				document.getElementById(args['insert']).appendChild(el[0]);
			}
			
			if(args['position'].indexOf('%')== -1) {
				var prb_w=args['position'];
			}
			else {
				var prb_w=Math.round(args['width']/100*args['position'].substr(0,args['position'].indexOf('%')));
			}
			var prb_h=args['height'];
			
			if(prb_w>args['width']) {
				prb_w=args['width'];
			}
			
			el[1]= document.createElement('div');
			el[1].setAttribute('id', 'progressbar_p_el_1');
			if(args['imgorcolor'].toLowerCase().indexOf('.gif')== -1 && args['imgorcolor'].toLowerCase().indexOf('.jpg')== -1 && args['imgorcolor'].toLowerCase().indexOf('.png')== -1 ) {
				el[1].setAttribute('style', 'width:'+prb_w+'px; height:'+prb_h+'px; border:none; background:'+args['imgorcolor']+';');
			}
			else {
				el[1].setAttribute('style', 'width:'+prb_w+'px; height:'+prb_h+'px; border:none; background:url('+args['imgorcolor']+');');
			}
			document.getElementById('progressbar_p_el_0').appendChild(el[1]);
			
		},
		setpos: function(pos) {
			if(pos.indexOf('%')== -1) {
				var prb_w=pos;
			}
			else {
				var prb_w=Math.round(this.width/100*pos.substr(0,pos.indexOf('%')));
			}
			
			if(prb_w>this.width) {
				prb_w=this.width;
			}
			document.getElementById('progressbar_p_el_1').style.width=prb_w+'px';
		},
		remove: function() {
			document.getElementById('progressbar_p_el_0').removeChild(document.getElementById('progressbar_p_el_1'));
			
			if(this.insert=='body') {
				document.body.removeChild(document.getElementById('progressbar_p_el_0'));
			}
			else {
				document.getElementById(this.insert).removeChild(document.getElementById('progressbar_p_el_0'));
			}
		}
	},
	movepanel: {
		width: 0,
		height: 0,
		speed: 0,
		step: 0,
		start: function(args) {
			args = args || {};
			var default_args = {
				'width': 640,
				'height': 480,
				'widthimg': 0,
				'heightimg': 0,
				'color': '#FF6600',
				'border': '#FF0000',
				'image': '',
				'speed': 10,
				'step': 15,
				'textcolor': '#555555',
				'text': 'Добро пожаловать на сайт!',
				'closecolor': '#FF0000',
				'close': 'закрыть'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.width=args['width'];
			this.height=args['height'];
			this.speed=args['speed'];
			this.step=args['step'];
			
			var el=[];
			var img_wh='';
			if(args['widthimg']!=0) {
				img_wh=img_wh+' width="'+args['widthimg']+'"';
			}
			if(args['heightimg']!=0) {
				img_wh=img_wh+' height="'+args['heightimg']+'"';
			}
			var img_div=args['height']-30;
			
			el[0]= document.createElement('div');
			el[0].setAttribute('id', 'movepanel_p_el_m');
			el[0].setAttribute('style', 'position:absolute; border:1px solid '+args['border']+'; top:0px; left:0px; width:'+args['width']+'px; height:'+args['height']+'px; text-align:center; background:'+args['color']+';');
			document.body.appendChild(el[0]);
				
			el[1]= document.createElement('div');
			el[1].setAttribute('id', 'movepanel_p_el_mt');
			el[1].setAttribute('style', 'height:30px; background:'+args['color']+';');
			document.getElementById('movepanel_p_el_m').appendChild(el[1]);
			el[1].innerHTML='<table width="100%" cellspacing="0" cellpadding="0"><tr><td width="100%"></td><td onclick="effect.movepanel.onclose();" style="cursor:pointer; text-align:center; border-left:1px solid '+args['border']+'; border-bottom:1px solid '+args['border']+'; padding-left:5px; padding-right:5px; color:'+args['closecolor']+'; background:'+args['color']+';">'+args['close']+'</td></tr></table>';
				
			el[2]= document.createElement('div');
			el[2].setAttribute('id', 'movepanel_p_el_mb');
			el[2].setAttribute('style', 'text-align:center; height:'+img_div+'px; background:'+args['color']+'; color:'+args['textcolor']+';');
			document.getElementById('movepanel_p_el_m').appendChild(el[2]);
			if(args['image']!='') {
				el[2].innerHTML='<table width="100%" height="100%"><tr><td><img src="'+args['image']+'"'+img_wh+' /></td></tr></table>';
			}
			else {
				el[2].innerHTML=args['text'];
			}
				
			window.onscroll = function() {
				effect.movepanel.getpos();
			}
				
			this.drawing();
		},
		drawing: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('movepanel_p_el_mt').style.visibility='hidden';
			document.getElementById('movepanel_p_el_mt').style.display='none';
			
			document.getElementById('movepanel_p_el_mb').style.visibility='hidden';
			document.getElementById('movepanel_p_el_mb').style.display='none';
			
			document.getElementById('movepanel_p_el_m').style.width=1+'px';
			document.getElementById('movepanel_p_el_m').style.top=main_top+'px';
			document.getElementById('movepanel_p_el_m').style.left=d_param[4]+d_param[0]-20+'px';
			
			setTimeout('effect.movepanel.movement_1();',this.speed);
		},
		movement_1: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('movepanel_p_el_m').style.top=main_top+'px';
			document.getElementById('movepanel_p_el_m').style.left=parseInt(document.getElementById('movepanel_p_el_m').style.left)-this.step+'px';
			document.getElementById('movepanel_p_el_m').style.width=parseInt(document.getElementById('movepanel_p_el_m').style.width)+this.step+'px';
			if(parseInt(document.getElementById('movepanel_p_el_m').style.width)>=this.width) {
				document.getElementById('movepanel_p_el_m').style.width=this.width+'px';
				setTimeout('effect.movepanel.movement_2();',this.speed);
			}
			else {
				setTimeout('effect.movepanel.movement_1();',this.speed);
			}
		},
		movement_2: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('movepanel_p_el_m').style.top=main_top+'px';
			document.getElementById('movepanel_p_el_m').style.left=parseInt(document.getElementById('movepanel_p_el_m').style.left)-this.step+'px';
			if(parseInt(document.getElementById('movepanel_p_el_m').style.left)<=main_left) {
				document.getElementById('movepanel_p_el_m').style.left=main_left+'px';
				
				document.getElementById('movepanel_p_el_mt').style.visibility='visible';
				document.getElementById('movepanel_p_el_mt').style.display='block';
			
				document.getElementById('movepanel_p_el_mb').style.visibility='visible';
				document.getElementById('movepanel_p_el_mb').style.display='block';
			}
			else {
				setTimeout('effect.movepanel.movement_2();',this.speed);
			}
		},
		movement_3: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('movepanel_p_el_m').style.top=main_top+'px';
			document.getElementById('movepanel_p_el_m').style.left=parseInt(document.getElementById('movepanel_p_el_m').style.left)-this.step+'px';
			if(parseInt(document.getElementById('movepanel_p_el_m').style.left)<=d_param[4]+0) {
				document.getElementById('movepanel_p_el_m').style.left=d_param[4]+0+'px';
				setTimeout('effect.movepanel.movement_4();',this.speed);
			}
			else {
				setTimeout('effect.movepanel.movement_3();',this.speed);
			}
		},
		movement_4: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			document.getElementById('movepanel_p_el_m').style.top=main_top+'px';
			document.getElementById('movepanel_p_el_m').style.left=d_param[4]+0+'px';
			if(parseInt(document.getElementById('movepanel_p_el_m').style.width)-this.step<=1) {
				document.getElementById('movepanel_p_el_m').style.width=1+'px';
			}
			else {
				document.getElementById('movepanel_p_el_m').style.width=parseInt(document.getElementById('movepanel_p_el_m').style.width)-this.step+'px';
			}
			if(parseInt(document.getElementById('movepanel_p_el_m').style.width)<=1) {
				document.getElementById('movepanel_p_el_m').style.visibility='hidden';
				effect.movepanel.remove();
			}
			else {
				setTimeout('effect.movepanel.movement_4();',this.speed);
			}
		},
		onclose: function() {
			document.getElementById('movepanel_p_el_mt').style.visibility='hidden';
			document.getElementById('movepanel_p_el_mt').style.display='none';
			
			document.getElementById('movepanel_p_el_mb').style.visibility='hidden';
			document.getElementById('movepanel_p_el_mb').style.display='none';
			
			setTimeout('effect.movepanel.movement_3();',this.speed);
		},
		remove: function() {
			document.getElementById('movepanel_p_el_m').removeChild(document.getElementById('movepanel_p_el_mt'));
			document.getElementById('movepanel_p_el_m').removeChild(document.getElementById('movepanel_p_el_mb'));
			
			document.body.removeChild(document.getElementById('movepanel_p_el_m'));
		},
		getpos: function() {
			var d_param=effect.noeffect.winparam();
			var main_left=Math.round(d_param[4]+(d_param[0]-this.width)/2);
			var main_top=Math.round(d_param[5]+(d_param[1]-this.height)/2);
			
			if(document.getElementById('movepanel_p_el_m')) {
				document.getElementById('movepanel_p_el_m').style.top=main_top+'px';
			}
		}
	},
	showimage: {
		full: true,
		start: function(args) {
			args = args || {};
			var default_args = {
				'width': 0,
				'height': 0,
				'color': '#555555',
				'image': '',
				'full': true
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			this.full=args['full'];
			
			var el=[];
			var img_wh='';
			if(args['width']!=0) {
				img_wh=img_wh+' width="'+args['width']+'"';
			}
			if(args['height']!=0) {
				img_wh=img_wh+' height="'+args['height']+'"';
			}
			
			el[0]= document.createElement('div');
			el[0].setAttribute('id', 'showimage_s_el_0');
			el[0].setAttribute('style', 'position:absolute; text-align:center; top:0px; left:0px; border:none; background:'+args['color']+';');
			document.body.appendChild(el[0]);
			el[0].innerHTML='<table width="100%" height="100%"><tr><td><img src="'+args['image']+'"'+img_wh+' /></td></tr></table>';
			
			el[0].onclick = function() {
				effect.showimage.remove();
			}
			
			window.onscroll = function() {
				effect.showimage.setpos();
			}
			
			this.drawing();
		},
		drawing: function() {
			var d_param=effect.noeffect.winparam();
			if(document.getElementById('showimage_s_el_0')) {
				if(this.full) {
					document.getElementById('showimage_s_el_0').style.width=d_param[4]+d_param[0]+'px';
					document.getElementById('showimage_s_el_0').style.height=d_param[5]+d_param[1]+'px';
				}
				else {
					document.getElementById('showimage_s_el_0').style.width=d_param[0]+'px';
					document.getElementById('showimage_s_el_0').style.height=d_param[1]+'px';
					document.getElementById('showimage_s_el_0').style.left=d_param[4]+0+'px';
					document.getElementById('showimage_s_el_0').style.top=d_param[5]+0+'px';
				}
			}
		},
		setpos: function() {
			if(!this.full) {
				effect.showimage.drawing();
			}
		},
		remove: function() {
			document.body.removeChild(document.getElementById('showimage_s_el_0'));
		}
	},
	toppanel: {
		browser: function() {
			return effect.noeffect.browser();
		},
		start: function(args) {
			args = args || {};
			var default_args = {
				'height': 25,
				'color': '#555555',
				'border': '#FF0000',
				'sizeborder': 1,
				'textcolor': '#FF6600',
				'text': 'Добро пожаловать на сайт!'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			var el=[];
			
			el[0]= document.createElement('div');
			el[0].setAttribute('id', 'toppanel_p_el_0');
			el[0].setAttribute('style', 'position:absolute; text-align:center; top:0px; left:0px; height:'+args['height']+'px; color:'+args['textcolor']+'; border:'+args['sizeborder']+'px solid '+args['border']+'; background:'+args['color']+';');
			document.body.appendChild(el[0]);
			el[0].innerHTML=args['text'];
			
			el[0].onclick = function() {
				effect.toppanel.remove();
			}
			
			window.onscroll = function() {
				effect.toppanel.drawing();
			}
			
			this.drawing();
		},
		drawing: function() {
			var d_param=effect.noeffect.winparam();
			if(document.getElementById('toppanel_p_el_0')) {
				document.getElementById('toppanel_p_el_0').style.width=d_param[0]-20+'px';
				document.getElementById('toppanel_p_el_0').style.left=d_param[4]+0+'px';
				document.getElementById('toppanel_p_el_0').style.top=d_param[5]+0+'px';
			}
		},
		remove: function() {
			document.body.removeChild(document.getElementById('toppanel_p_el_0'));
		}
	},
	accordion: {
		rand_name: '',
		start: function(args) {
			args = args || {};
			var default_args = {
				'count': 3,
				'width': 300,
				'height': 150,
				'insert': 'body',
				'color': '#555555',
				'border': '#FF0000',
				'sizeborder': 1,
				'titlecolor': '#FF5555',
				'titletcolor': '#FF0000',
				'textcolor': '#FF6600',
				'titletext': ['Заголовок 1',
							  'Заголовок 2',
							  'Заголовок 3'],
				'text': ['Текст 1',
						 'Текст 2',
						 'Текст 3']
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			var alf ='abcdefghijklmnopqrstuvwxyz1234567890';
			this.rand_name='';
			for(var i=0;i<10;i++) {
				this.rand_name=this.rand_name+alf.charAt(effect.noeffect.winrand(0,alf.length-1));
			}
			
			var elmn;
				elmn= document.createElement('div');
				elmn.setAttribute('id', 'accordion_s_el_m'+this.rand_name);
				elmn.setAttribute('style', 'border:none;');
				if(args['insert']=='body') {
					document.body.appendChild(elmn);
				}
				else {
					document.getElementById(args['insert']).appendChild(elmn);
				}
				
			var inhtml='';
			for(var i=0;i<args['count'];i++) {
				accordion_on_event[accordion_num_add]=i;
				accordion_on_eventid[accordion_num_add]=this.rand_name;
				accordion_on_eventkey[accordion_num_add]=false;
				inhtml=inhtml+'<div id="accordion_s_el_mt'+i+this.rand_name+'" style="width:'+args['width']+'px; height:30px; text-align:center; cursor:pointer; border-top:'+args['sizeborder']+'px solid '+args['border']+'; border-left:'+args['sizeborder']+'px solid '+args['border']+'; border-right:'+args['sizeborder']+'px solid '+args['border']+'; background:'+args['titlecolor']+'; color:'+args['titletcolor']+';" onclick="effect.accordion.onclick(\'accordion_s_el_mb'+accordion_on_event[accordion_num_add]+accordion_on_eventid[accordion_num_add]+'\','+accordion_num_add+');">'+args['titletext'][i]+'</div>';
				
				inhtml=inhtml+'<div id="accordion_s_el_mb'+i+this.rand_name+'" style="width:'+args['width']+'px; height:'+(args['height']-30)+'px; display:none; text-align:center; border:'+args['sizeborder']+'px solid '+args['border']+'; background:'+args['color']+'; color:'+args['textcolor']+';">'+args['text'][i]+'</div>';
				
				accordion_num_add++;
			}
			elmn.innerHTML=inhtml;
			
		},
		onclick: function(id,num) {
			if(accordion_on_eventkey[num]) {
				document.getElementById(id).style.display='none';
				accordion_on_eventkey[num]=false;
			}
			else {
				document.getElementById(id).style.display='block';
				accordion_on_eventkey[num]=true;
			}
		}
	},
	noeffect: {
		winparam: function() {
			var w_w = (window.innerWidth ? window.innerWidth : (document.documentElement.clientWidth ? document.documentElement.clientWidth : document.body.offsetWidth));
			var w_h = (window.innerHeight ? window.innerHeight : (document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.offsetHeight));
			
			var s_w = document.body.scrollWidth;
			var s_h = document.body.scrollHeight;
			
			var s_l = self.pageXOffset || (document.documentElement && document.documentElement.scrollLeft) || (document.body && document.body.scrollLeft);
			var s_t = self.pageYOffset || (document.documentElement && document.documentElement.scrollTop) || (document.body && document.body.scrollTop);
			
			return [w_w,w_h,s_w,s_h,s_l,s_t];
		},
		winrand: function(rmin, rmax) {
			return Math.floor(Math.random() * (rmax - rmin + 1)) + rmin;
		},
		browser: function() {
			if(navigator.appName == 'Microsoft Internet Explorer' || navigator.userAgent.indexOf('MSIE')!= -1) {
				return true;
			}
			else {
				return false;
			}
		},
		browsername: function () {
			var useragent=navigator.userAgent;
			var navigatorname;
			if(useragent.indexOf('MSIE')!= -1) {
				navigatorname="MSIE";
			}
			else if(useragent.indexOf('Safari')!= -1) {
				navigatorname="Safari";
			}
			else if(useragent.indexOf('Gecko')!= -1) {
				if(useragent.indexOf('Chrome')!= -1) {
					navigatorname="Google Chrome";
				}
				else {
					navigatorname="Mozilla";
				}
			}
			else if(useragent.indexOf('Mozilla')!= -1) {
				navigatorname="old Netscape or Mozilla";
			}
			else if(useragent.indexOf('Opera')!= -1) {
				navigatorname="Opera";
			}
			return navigatorname;
		}
	}
};

var modules = {
	chat: {
		start: function(args) {
			args = args || {};
			var default_args = {
				'setid': 'modules_chat',
				'border': '#FF6600',
				'sizeborder': 1,
				'width': 550,
				'height': 450,
				'leftwidth': 550,
				'leftheight': 450,
				'rightheight': 450,
				'insert': 'body',
				'borders': '#FF6600',
				'chatcolor': '#FFFFFF',
				'color': '#FFFFFF'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			args['width']=args['width']+220;
			args['height']=args['height']+250;
			
			var elmn;
				elmn= document.createElement('div');
				elmn.setAttribute('id', args['setid']);
				elmn.setAttribute('style', 'border:none;');
				if(args['insert']=='body') {
					document.body.appendChild(elmn);
				}
				else {
					document.getElementById(args['insert']).appendChild(elmn);
				}
				
			args['borders']=args['borders'].substr(1);
			args['chatcolor']=args['chatcolor'].substr(1);
			args['color']=args['color'].substr(1);
			
			var inhtml='<iframe style="border:'+args['sizeborder']+'px solid '+args['border']+';" scrolling="no" src="http://nagon.net/modules_chat.php?wl='+args['leftwidth']+'&hl='+args['leftheight']+'&hr='+args['rightheight']+'&zb='+args['borders']+'&zc='+args['chatcolor']+'&zd='+args['color']+'" width="'+args['width']+'" height="'+args['height']+'"  frameborder="0"></iframe>';
			
			elmn.innerHTML=inhtml;
		}
	},
	sound: {
		start: function(args) {
			args = args || {};
			var default_args = {
				'music': 'http://nagon.net/mus/0017.mp3'
			}
			
			for(var index in default_args) {
				if(typeof args[index] == "undefined") args[index] = default_args[index];
			}
			
			var elmn;
				elmn= document.createElement('div');
				elmn.setAttribute('id', 'sound_s_el_m');
				elmn.setAttribute('style', 'border:none;');
				document.body.appendChild(elmn);
			
			var inhtml='<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" width="16" height="16" id="m_player" align="middle">'+
				'<param name="allowScriptAccess" value="sameDomain" />'+
				'<param name="allowFullScreen" value="false" />'+
				'<param name="movie" value="http://nagon.net/flash/player_mod.swf" />'+
				'<param name="flashvars" value="m='+decodeURI(args['music'])+'" />'+
				'<param name="quality" value="high" />'+
				'<param name="bgcolor" value="#ffffff" />'+
				'<embed src="http://nagon.net/flash/player_mod.swf" flashvars="m='+decodeURI(args['music'])+'" quality="high" bgcolor="#ffffff" width="1" height="1" name="player_mod" align="middle" allowScriptAccess="sameDomain" allowFullScreen="false" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />'+
	'</object>';
			elmn.innerHTML=inhtml;
		},
		stop: function() {
			if(document.getElementById('sound_s_el_m')) {
				document.body.removeChild(document.getElementById('sound_s_el_m'));
			}
		}
	}
};

var cooker = {
	set: function(cookie_name, cookie_value, cookie_expires, cookie_path, cookie_domain, cookie_secure) {
		if(cookie_name!==undefined) {
			cookie_expires=cookie_expires || 0;
			var expire_date = new Date;
			expire_date.setTime(expire_date.getTime() + (cookie_expires*1000));
			document.cookie = cookie_name + "=" + escape(cookie_value)+'; ' + 
			((cookie_expires === undefined) ? '' : 'expires=' + expire_date.toGMTString()+'; ') +
			((cookie_path === undefined) ? 'path=/;' : 'path='+cookie_path+'; ') +
			((cookie_domain === undefined) ? '' : 'domain='+cookie_domain+'; ') +
			((cookie_secure === true) ? 'secure; ' : '');
		}
	},
	get: function(cookie_name) {
		var cookie = document.cookie, length = cookie.length;
		if(length) {
			var cookie_start = cookie.indexOf(cookie_name + '=');
			if(cookie_start != -1) {
				var cookie_end = cookie.indexOf(';', cookie_start);
				if(cookie_end == -1) {
					cookie_end = length;
				}
				cookie_start += cookie_name.length + 1;
				return unescape(cookie.substring(cookie_start, cookie_end));
			}
		}
	},
	erase: function(cookie_name) {
		cooker.set(cookie_name, '', -1);
	},
	test: function() {
		cooker.set('test_cookie', 'test', 10);
		var work = (cooker.get('test_cookie') === 'test') ? true : false;
		cooker.erase('test_cookie');
		return work;
	}
};
