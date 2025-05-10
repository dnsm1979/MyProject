$(document).ready(function() {
    $('#image-upload-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Обновление галереи без перезагрузки
                $('#image-gallery').load(location.href + ' #image-gallery');
            }
        });
    });
});