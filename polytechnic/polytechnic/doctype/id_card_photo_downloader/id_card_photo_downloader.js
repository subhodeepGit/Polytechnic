// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('ID Card Photo Downloader', {
	class_stream(frm){
        if (frm.doc.class_stream && frm.doc.session){
            frappe.call({
                method: "polytechnic.polytechnic.doctype.id_card_photo_downloader.id_card_photo_downloader.get_documents",
                args: {
                    class_stream: frm.doc.class_stream,
                    session:frm.doc.session
                },
            
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'student_photos');
                        (r.message).forEach(element => {
                            var c = frm.add_child("student_photos")
                            c.student=element.student
                            c.student_name=element.student_name
                            c.student_roll_number=element.roll_no
							c.student_passport_photo=element.passport_photo
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("student_photos")
                } 
                
            }); 
        }
    },
	refresh(frm) {
		frm.fields_dict["student_photos"].grid.add_custom_button(__('Download Photos'), 
			function() {
				let selected = frm.get_selected();
				// alert(JSON.stringify(selected));
				let sel = selected["student_photos"];
				// alert(sel);

				// code to download all rows
				// for (var i = 0; i < cur_frm.doc.student_photos.length; i++) {
				// 	if (cur_frm.doc.student_photos[i].student_passport_photo) {
				// 	const data = cur_frm.doc.student_photos[i].student_passport_photo;
				// 	const roll = cur_frm.doc.student_photos[i].student_roll_number;
				// 	const a = document.createElement('a');
				// 	a.href = data;
				// 	a.download = data.split('/').pop();
				// 	a.setAttribute('download', roll);
				// 	document.body.appendChild(a);
				// 	a.click();
				// 	document.body.removeChild(a);
				// 	}
				// 	}


				// code to download selected rows
				for (var i = 0; i < cur_frm.doc.student_photos.length; i++) {
					// alert(cur_frm.doc.student_photos[i].name)
					for (var j = 0; j < sel.length; j++) {
						if(sel[j]==cur_frm.doc.student_photos[i].name){
							// alert(cur_frm.doc.student_photos[i].name)
							const data = cur_frm.doc.student_photos[i].student_passport_photo;
							const roll = cur_frm.doc.student_photos[i].student_roll_number;
							const a = document.createElement('a');
							a.href = data;
							a.download = data.split('/').pop();
							a.setAttribute('download', roll);
							document.body.appendChild(a);
							a.click();
							document.body.removeChild(a);
						}
					}
					}
        });
        frm.fields_dict["student_photos"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
	}
});

