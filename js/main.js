if (typeof jQuery != "undefined") {
	
	/* 1.Funciones a ejecutar en la carga de página
	---------------------------------------------------------------------------------- */
	jQuery(function() {
		jQuery('table th.fecha').append('<a href="#">v</a>').find('a').bind('click', function(e) {
			var target = jQuery(this).parents('tr:first').next('tr').next('tr').next('tr').next('tr').next('tr').find('th.fecha');
			
			if (target.length > 0) {
				jQuery.scrollTo(target, 250);
			} else {
				jQuery.scrollTo(jQuery('th.fecha:first'), 250);
			}
			
			e.preventDefault();
		});
		
		jQuery('table th.fecha:last a').html('∧');
	});
	
}