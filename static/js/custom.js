$(document).ready(function(){

    $('.add_todo').on('click', function(e){
        e.preventDefault();
        var title = document.getElementById('id_title').value
        var url = document.getElementById('add_to_do').value
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        // console.log(title, url, csrf_token)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'title':title,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                if(response.status == 'success'){
                    // console.log(response)
                    html='<ul class="list-group list-group-horizontal rounded-0 bg-transparent"><li class="list-group-item d-flex align-items-center ps-0 pe-3 py-1 rounded-0 border-0 bg-transparent"><div class="form-check"><input class="form-check-input me-0" type="checkbox" value="" id="flexCheckChecked1" aria-label="..." checked /></div></li><li class="list-group-item px-3 py-1 d-flex align-items-center flex-grow-1 border-0 bg-transparent"><p class="lead fw-normal mb-0">'+response.title+'</p></li><li class="list-group-item ps-3 pe-0 py-1 rounded-0 border-0 bg-transparent"><div class="d-flex flex-row justify-content-end mb-1"><a href="#!" class="text-success" data-mdb-toggle="tooltip" title="complete todo"><i class="fa-solid fa-check me-3"></i></a><a href="#!" class="text-info" data-mdb-toggle="tooltip" title="Edit todo"><i class="fas fa-pencil-alt me-3"></i></a><a href="#!" class="text-danger" data-mdb-toggle="tooltip" title="Delete todo"><i class="fas fa-trash-alt"></i></a></div><div class="text-end text-muted"><a href="#!" class="text-muted" data-mdb-toggle="tooltip" title="Created date"><p class="small mb-0"><i class="fas fa-info-circle me-2"></i>'+response.created_at+'</p> </a></div></li></ul>'
                }
                $('.todo_list_block').append(html)
                document.getElementById('id_form_title').reset();
                
            }
        })
    })
})