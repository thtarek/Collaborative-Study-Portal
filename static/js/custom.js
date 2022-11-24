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
                    html='<ul id="todo-'+response.id+'" class="list-group list-group-horizontal rounded-0 bg-transparent"><li class="list-group-item d-flex align-items-center ps-0 pe-3 py-1 rounded-0 border-0 bg-transparent"><div class="form-check"><i class="fa-solid fa-circle me-0"></i></div></li><li class="list-group-item px-3 py-1 d-flex align-items-center flex-grow-1 border-0 bg-transparent"><p class="lead fw-normal mb-0" id="checkbox-'+response.id+'">'+response.title+'</p></li><li class="list-group-item ps-3 pe-0 py-1 rounded-0 border-0 bg-transparent"><div class="d-flex flex-row justify-content-end mb-1"><a href="#!" class="text-success complete_todo" data-url="/base/to-do/complete/'+response.id+'/" data-mdb-toggle="tooltip" id="completebtn-'+response.id+'"  title="complete todo"><i class="fa-solid fa-circle-check me-3"></i></a><a href="/base/to-do/edit-todo/'+response.id+'/" class="text-info" data-mdb-toggle="tooltip" title="Edit todo"><i class="fas fa-pencil-alt me-3"></i></a><a href="#!" class="text-danger delete_todo" data-url="/base/to-do/delete/'+response.id+'/" data-mdb-toggle="tooltip" title="Delete todo"><i class="fas fa-trash-alt"></i></a></div><div class="text-end text-muted"><a href="#!" class="text-muted" data-mdb-toggle="tooltip" title="Created date"><p class="small mb-0"><i class="fas fa-info-circle me-2"></i>'+response.created_at+'</p> </a></div></li></ul>'
                }
                $('.todo_list_block').append(html)
                document.getElementById('id_form_title').reset();
                
            }
        })
    })

    $(document).on('click', '.delete_todo', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        // alert(url)
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == "success"){
                    document.getElementById('todo-'+response.id).remove()
                }
                // console.log(response)
            }
        })
    })
    // complete_todo
    $(document).on('click', '.complete_todo', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'success'){
                    the_id = 'checkbox-'+response.id
                    completebtn_id = 'completebtn-'+response.id
                    $('#'+the_id).addClass('text-decoration-line-through');
                    $('#'+completebtn_id).addClass('visually-hidden');
                }

            }
        })
       
    })
    // end complete_todo
})