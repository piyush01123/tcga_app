$("document").ready(function(){

    $("#tcgaimg").change(function() {
      console.log("SHOULD RUN");
      $('#inp_img').attr('src', window.URL.createObjectURL(this.files[0]));
      var form = new FormData();
      var fileInputElement = document.getElementById('tcgaimg');
      form.append("img", fileInputElement.files[0]);
      $.ajax({
                type: 'POST',
                url: `/predict`,
                processData: false,
                contentType: false,
                async: true,
                cache: false,
                data: form,
                success: function (data) {
                  console.log(data);
                  document.getElementById('out_img_a').src = "data:image/png;base64,"+data["BRCA"]["gradcam_base64"];
                  document.getElementById('out_text_a').textContent = "Predicted class: "+data["BRCA"]["pred"];

                  document.getElementById('out_img_b').src = "data:image/png;base64,"+data["COAD"]["gradcam_base64"];
                  document.getElementById('out_text_b').textContent = "Predicted class: "+data["COAD"]["pred"];

                  document.getElementById('out_img_c').src = "data:image/png;base64,"+data["KICH"]["gradcam_base64"];
                  document.getElementById('out_text_c').textContent = "Predicted class: "+data["KICH"]["pred"];

                  document.getElementById('out_img_d').src = "data:image/png;base64,"+data["KIRC"]["gradcam_base64"];
                  document.getElementById('out_text_d').textContent = "Predicted class: "+data["KIRC"]["pred"];

                  document.getElementById('out_img_e').src = "data:image/png;base64,"+data["KIRP"]["gradcam_base64"];
                  document.getElementById('out_text_e').textContent = "Predicted class: "+data["KIRP"]["pred"];

                  document.getElementById('out_img_f').src = "data:image/png;base64,"+data["LIHC"]["gradcam_base64"];
                  document.getElementById('out_text_f').textContent = "Predicted class: "+data["LIHC"]["pred"];

                  document.getElementById('out_img_g').src = "data:image/png;base64,"+data["LUAD"]["gradcam_base64"];
                  document.getElementById('out_text_g').textContent = "Predicted class: "+data["LUAD"]["pred"];

                  document.getElementById('out_img_h').src = "data:image/png;base64,"+data["LUSC"]["gradcam_base64"];
                  document.getElementById('out_text_h').textContent = "Predicted class: "+data["LUSC"]["pred"];

                  document.getElementById('out_img_i').src = "data:image/png;base64,"+data["PRAD"]["gradcam_base64"];
                  document.getElementById('out_text_i').textContent = "Predicted class: "+data["PRAD"]["pred"];

                  document.getElementById('out_img_j').src = "data:image/png;base64,"+data["READ"]["gradcam_base64"];
                  document.getElementById('out_text_j').textContent = "Predicted class: "+data["READ"]["pred"];

                  document.getElementById('out_img_k').src = "data:image/png;base64,"+data["STAD"]["gradcam_base64"];
                  document.getElementById('out_text_k').textContent = "Predicted class: "+data["STAD"]["pred"];
                }
            })
    });
});
