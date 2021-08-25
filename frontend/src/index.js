// import React from 'react';
// import ReactDOM from 'react-dom';

const person = {
	talk() { 
		var self = this;
		setTimeout(function() {
			console.log('self', self);
		}, 1000);
	}
};

person.talk()
