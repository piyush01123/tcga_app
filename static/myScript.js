$("document").ready(function(){

    $("#tcgaimg").change(function() {
      console.log("SHOULD RUN");
      $('#inp_img').attr('src', window.URL.createObjectURL(this.files[0]));
      var form = new FormData();
      var fileInputElement = document.getElementById('tcgaimg');
      form.append("img", fileInputElement.files[0]);
      $.ajax({
                type: 'POST',
                url: `/classify`,
                processData: false,
                contentType: false,
                async: false,
                cache: false,
                data: form,
                success: function (data) {
                  console.log("Success");
                  console.log(data["gradcam_base64"], data["gradcam_base64"]);
                  document.getElementById('out_img').src = "data:image/png;base64,"+data["gradcam_base64"];
                  document.getElementById('out_text').textContent = "Predicted class: "+data["pred"];
                  // document.getElementById('out_img').src = "http://localhost:8080/static/outdir/test.png";
                  // document.getElementById('out_text').textContent = "Predicted class cancer";
                  }
            })
    });
});
