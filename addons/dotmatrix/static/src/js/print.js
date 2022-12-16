// odoo.define('dotmatrix.print_button', function (require) {
//     'use strict';

//     var FromController = require('web.FormController');

//     FromController.include({
//         _onButtonClicked: function (event) {

//             console.log(event);
//             if (event.data.attrs.custom === 'print_dotmatrix') {
//                 var print_data = event.data.record.data.print_data;
//                 if (!print_data) {
//                     alert("No printer data found, please click refresh button!");
//                     return;
//                 }

//                 console.log(print_data);

//                 $.ajax({
//                     url: 'http://localhost:8080/dotmatrix/print',
//                     type: 'POST',
//                     data: {
//                         'print_data': print_data
//                     },
//                     success: function (data) {
//                         alert("Print success!");
//                     },
//                     error: function (data) {
//                         alert("Print failed!Please check the printer proxy!");
//                         console.log(data);
//                     }

//                 });
//             }

//             this._super(event);
//         },
//     });

// });