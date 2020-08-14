$(document).ready(function(){

    $(".upload-btn").on("click", function(event){
        $("#modal_form_blueprint").modal('show');
        // console.log($(this).parent().parent().find('.oderId').val());
        $("#modal_form_blueprint input[name='orderid']").val($(this).parent().parent().find('.oderId').val());
        // $("#modal_form_photos_list").modal('show');
        $('#modal_form_blueprint #upload_filename').text('');
        $("#modal_form_blueprint input[name='airbnb']").removeAttr("disabled");
        $("#modal_form_blueprint input[name='airbnb']").text('');
        $("#modal_form_blueprint input[name='google_drive']").removeAttr("disabled");
        $("#modal_form_blueprint input[name='google_drive']").text('');

    });

    $("#blueprint-upload-btn").on("click", function(event){
        event.preventDefault();

        var rawImageUrl = $("#modal_form_blueprint input[name='rawImageUrl']").val();
        var orderid = $("#modal_form_blueprint input[name='orderid']").val();
        var airbnb = $("#modal_form_blueprint input[name='airbnb']").val();
        var google_drive = $("#modal_form_blueprint input[name='google_drive']").val();
        
        $.ajax({
            url: '/uploadscan/',
            method: 'POST',
            data: {
                rawImageUrl: rawImageUrl,
                orderid: orderid,
                airbnb: airbnb,
                google_drive:google_drive,
                csrfmiddlewaretoken:$('#modal_form_blueprint input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(response){
                
                if(response.success == true){
                    $('#modal_form_blueprint').modal('hide');
                    $('#modal_form_blueprint_submitted').modal('show');
                }
            }
        });
    });

    // uploading detail after being saved scanTitle
    $('#productTitleBtn').on("click", function(){
        var orderid = $("#modal_form_blueprint input[name='orderid']").val();
        var productTitle = $('#modal_form_blueprint_submitted #productTitle').val();
        if(productTitle){
            $.ajax({
                url: '/uploadtitle/',
                method: 'POST',
                data: {
                    orderid: orderid,
                    productTitle: productTitle,
                    csrfmiddlewaretoken:$('#modal_form_blueprint_submitted input[name=csrfmiddlewaretoken]').val(),
                },
                success:function(response){
                    if(response.success == true){
                        console.log(response.type);
                        var scanTitle = response.scan.title;
                        console.log(scanTitle);
                        switch (response.type) {
                            case 2:
                            case 3:
                                $("#modal_form_blueprint_submitted").modal("hide");
                                $('#modal_form_upload_photos').modal("show");
                                break;
                            case 1:
                                $("#modal_form_blueprint_submitted").modal("hide");
                                break;
                            case 0:
                                break;
                            default:
                                break;
                        }
                        $('#modal_form_upload_photos .proj-title').text(response.scan.title);
                        $('#modal_form_upload_photos .proj-scan-img').attr("src", response.scan.scanImageUrl);
                        $("#modal_form_upload_photos input[name='proj-scan-id']").val(response.scan.id);
                    }
                }
            })
        }

    });

    // ajax for get detail list with respect to scan 
    // get : scan_id  ----- put : detail list
    $('#modal_form_upload_photos #show_photoslist_btn').on('click', function(){
        var scan_id = $("#modal_form_upload_photos input[name='proj-scan-id']").val();
        if(scan_id){
            $.ajax({
                url: '/getDatailbyId/',
                method: 'POST',
                data: {
                    scan_id: scan_id,
                    csrfmiddlewaretoken:$('#modal_form_upload_photos input[name=csrfmiddlewaretoken]').val(),
                },

                success:function(response){
                    if(response.success == true){
                        show_photos_list();
                        console.log(response.details.length);
                        for(var index = 0; index < response.details.length; index++){
                            $("#modal_form_photos_list .photos-wrapper").append('<li class="photo-item col-lg-6 col-md-6 col-sm-6 col-6"><img class="photo" src="'+response.details[index].scanDetailImageRaw+'"><div class="photo-action"><span class="title">Kitchen</span><img class="btn-remove" src="/static/img/garbage.png"></div></li>');
                        }
                    }
                }
            });
        }
    });

    // upload detail image and description of course title
    // get : scan_id, image url --- response : detial id, success 

    // console.log($("#photos-list-form"))
    $("#photos-list-form").on('click', ".btn-remove",function(event){
        event.preventDefault();
        $(this).parents('.photo-item').remove();
    })


    var obj = $(".blueprint-drag");
    obj.on('dragenter', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function (e) 
    {
         e.stopPropagation();
         e.preventDefault();
    });
    obj.on('drop', function (e) 
    {
         $(this).css('border', '2px dotted #0B85A1');
         e.preventDefault();
         var files = e.originalEvent.dataTransfer.files;
         for(var i = 0; i < files.length; i++){
            console.log(files[i]);
         }
         //We need to send dropped files to Server
         //handleFileUpload(files,obj);
    });
    
    $(document).on('dragenter', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
    });
    
    $(document).on('dragover', function (e) 
    {
      e.stopPropagation();
      e.preventDefault();
      obj.css('border', '2px dotted #0B85A1');
    });

    $(document).on('drop', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
    });
     
}); 



function show_blueprint_submitted()
{
    $("#modal_form_blueprint").modal('hide');
    $("#modal_form_blueprint_submitted").modal('show');
}

function show_photos_list()
{
    $("#modal_form_upload_photos").modal('hide');
    $("#modal_form_photos_list").modal('show');
}

function show_upload_photos(){
    $("#modal_form_blueprint_submitted").modal('hide');
    $("#modal_form_upload_photos").modal('show');
}

function show_photos_add()
{
    $("#modal_form_photos_list").modal('hide');
    $("#modal_form_photos_add").modal('show');
}

function sendFileToServer(formData,status)
{
    var uploadURL ="http://localhost:8000/uploadingScan"; //Upload URL
    var extraData ={}; //Extra Data.
    var jqXHR=$.ajax({
            xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                    xhrobj.upload.addEventListener('progress', function(event) {
                        var percent = 0;
                        var position = event.loaded || event.position;
                        var total = event.total;
                        if (event.lengthComputable) {
                            percent = Math.ceil(position / total * 100);
                        }
                        //Set progress
                        status.setProgress(percent);
                    }, false);
                }
            return xhrobj;
        },
    url: uploadURL,
    type: "POST",
    contentType:false,
    processData: false,
        cache: false,
        data: formData,
        success: function(data){
            status.setProgress(100);
 
            $("#status1").append("File upload Done<br>");         
        }
    }); 
 
    status.setAbort(jqXHR);
}
 
var rowCount=0;
function createStatusbar(obj)
{
     rowCount++;
     var row="odd";
     if(rowCount %2 ==0) row ="even";
     this.statusbar = $("<div class='statusbar "+row+"'></div>");
     this.filename = $("<div class='filename'></div>").appendTo(this.statusbar);
     this.size = $("<div class='filesize'></div>").appendTo(this.statusbar);
     this.progressBar = $("<div class='progressBar'><div></div></div>").appendTo(this.statusbar);
     this.abort = $("<div class='abort'>Abort</div>").appendTo(this.statusbar);
     obj.after(this.statusbar);
 
    this.setFileNameSize = function(name,size)
    {
        var sizeStr="";
        var sizeKB = size/1024;
        if(parseInt(sizeKB) > 1024)
        {
            var sizeMB = sizeKB/1024;
            sizeStr = sizeMB.toFixed(2)+" MB";
        }
        else
        {
            sizeStr = sizeKB.toFixed(2)+" KB";
        }
 
        this.filename.html(name);
        this.size.html(sizeStr);
    }
    this.setProgress = function(progress)
    {       
        var progressBarWidth =progress*this.progressBar.width()/ 100;  
        this.progressBar.find('div').animate({ width: progressBarWidth }, 10).html(progress + "% ");
        if(parseInt(progress) >= 100)
        {
            this.abort.hide();
        }
    }
    this.setAbort = function(jqxhr)
    {
        var sb = this.statusbar;
        this.abort.click(function()
        {
            jqxhr.abort();
            sb.hide();
        });
    }
}

function handleFileUpload(files,obj)
{
   for (var i = 0; i < files.length; i++) 
   {
        var fd = new FormData();
        fd.append('file', files[i]);
 
        var status = new createStatusbar(obj); //Using this we can set progress.
        status.setFileNameSize(files[i].name,files[i].size);
        // sendFileToServer(fd,status);
 
   }
}