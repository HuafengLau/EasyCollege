$(document).ready(function(){   
    
	$(function () {
	  $.scrollUp({
		scrollName: 'scrollUp', // Element ID
        scrollDistance: 300, // Distance from top/bottom before showing element (px)
        scrollFrom: 'top', // 'top' or 'bottom'
        scrollSpeed: 300, // Speed back to top (ms)
        easingType: 'linear', // Scroll to top easing (see http://easings.net/)
        animation: 'fade', // Fade, slide, none
        animationInSpeed: 200, // Animation in speed (ms)
        animationOutSpeed: 200, // Animation out speed (ms)
        scrollText: '回到顶部', // Text for element, can contain HTML
        scrollTitle: false, // Set a custom <a> title if required. Defaults to scrollText
        scrollImg: false, // Set true to use image
        activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
        zIndex: 2147483647 // Z-Index for the overlay
	  });
	});
	
	
	$('.ID_card').on('click', function(){
		var id=$(this).attr('id');  
		$.get('/index/get_idCard/', {'id':id}, function(data){
            $('#idCard_div').html(data);				
		});
		$('#idCard_modal').modal('show');
	});
	
	$('.need_login').on('click', function(){
		alert('请登陆后再使用此功能！');
	});
	
	$('.tooltip_p').each( function(){
        
        $(this).tooltip();
    });
	
    // JS for base.html   
    
    // JS for log.html
    
    // JS for register.html
    $("#register_sure_pwd").on('blur', function(){	
		var pwd1 = $("#register_stu_pwd").val();
		var pwd2 = $("#register_sure_pwd").val();
		if (pwd2 != pwd1){
			$('#register_check_pwd').html("<span class='glyphicon glyphicon-remove font-red'> 两次密码不一致！</span>");
		}else{
			$('#register_check_pwd').html("<span class='glyphicon glyphicon-ok font-green'> 两次密码一致</span>");
		}
	});
	
	$("#getCredit_mm").on('blur', function(){	
		var zh = $("#getCredit_zh").val();
		var mm = $("#getCredit_mm").val();
		if (zh != '' && mm != ''){
			$.get('/index/loading_gif/', {'loading':'true'}, function(data){
                $('#register_check_URP').html(data);
				$('#register_check_URP').append('<span>正在检测账号和密码</span>')
			});
			$.get('/index/verify_URP/', {'zh': zh,'mm':mm}, function(data){
               $('#register_check_URP').html(data);
            });
		}
		if (zh == '' && mm == ''){
			$('#register_check_URP').html('');
		}
	});
	
	$("#getCredit_zh").on('blur', function(){	
		var zh = $("#getCredit_zh").val();
		var mm = $("#getCredit_mm").val();
		if (zh != '' && mm != ''){
			$.get('/index/loading_gif/', {'loading':'true'}, function(data){
                $('#register_check_URP').html(data);
				$('#register_check_URP').append('<span>正在检测账号和密码</span>')
			});
			$.get('/index/verify_URP/', {'zh': zh,'mm':mm}, function(data){
                $('#register_check_URP').html(data);
            });
		}
		if (zh == '' && mm == ''){
			$('#register_check_URP').html('');
		}
	});
	
	$("#getCredit_mm").on('focus', function(){	
		var zh = $("#getCredit_zh").val();
		var mm = $("#getCredit_mm").val();
		if (zh != '' || mm != ''){
			$.get('/index/loading_gif/', {'loading':'true'}, function(data){
                $('#register_check_URP').html(data);
				$('#register_check_URP').append('<span>准备检测账号和密码</span>')
			});
		}
	});
	
	$("#getCredit_zh").on('focus', function(){	
		var zh = $("#getCredit_zh").val();
		var mm = $("#getCredit_mm").val();
		if (zh != '' || mm != ''){
			$.get('/index/loading_gif/', {'loading':'true'}, function(data){
                $('#register_check_URP').html(data);
				$('#register_check_URP').append('<span>准备检测账号和密码</span>')
			});
		}
	});
	
	
	
	$('#register_email').on('blur', function(){
		var search_str = /^[\w\-\.]+@[\w\-\.]+(\.\w+)+$/;
		var email_val = $("#register_email").val();
		if(search_str.test(email_val)){
			$.get('/log/verify_email/', {'email': email_val}, function(data){
                $('#register_check_emial').html(data);
            });
		}else{
			$('#register_check_emial').html("<span class='glyphicon glyphicon-remove font-red'> 请输入正确的邮箱地址</span>");
		}
	});
	
    // JS for center.html
    $(function () {
		$('#centerTab a:first').tab('show')
    })
	
	// JS for the change nic_name
    $('#change_nicname_btn').on('click', function(){
        var name = $('#nic_name_input').val();
        if (name==''){
            alert('昵称不能为空!');
        }
        else{
            var count=name.length; 
            if (count>10){
                alert('昵称不能超过10个字!');
            }else{
                $.get('/center/', {'nic_name':name},function(data){
					alert(data)
				}); 
				$('#center_name').html(name);
				$('#nic_name_input').val('')
            }
        }
    });
	
	//JS for change show_email
	$('#change_showEmail').on('click', function(){
		var text=$(this).text()
		var count = text.length;
		if (count == 11){
			$.post('/center/', {'change':'show_email'});
			var text=$(this).text('当前为不显示（点击更改）');
			alert('更改成功！');
		}else{
			$.post('/center/', {'change':'show_email'});
			var text=$(this).text('当前为显示（点击更改）');
			alert('更改成功！');
		}
	});
	
	$('#change_sign_btn').on('click',function(){
		var text=$('#sign_textarea').val()
		var count = text.length;
		if (count == 0){
			alert('个性签名不能为空！');
		}else if (count <= 50){
			$('#sign_textarea').val('');
			$('#center_sign').html(text);
			$.get('/center/', {'sign':text},function(data){
				alert(data);
			});
		}else{
			alert('不能超过50个字哦！');
		}
	
	});
	
    //JS for index.html
    //Edit the course_teacher
    $('.btn_edit_teacher').bind('click',function(){
        var id = $(this).parent().attr('id');     
        html = $(this).detach();       
        $('#'+id).html("<input class='input_add_teacher' type='text' id='' name='teacher_name' placeholder='输入后回车即可' autofocus>");

		$('#'+id).on('keypress', ".input_add_teacher", function (e) { 
			var name;
			name = $(this).val();
			
			var key = e.which; 
			if (key == 13) {
				if (name ==''){
			
					$(this).parent().html(html);
				}else{             
					$.post('/index/', {'course_id':id, 'teacher_name':name});
					var script;
					script = "<script>$('.click_info').on('click',function(){alert('你已经编辑过此项，刷新页面后可再次编辑')});</script>"
					$(this).parent().html("<button class='btn click_info' data-toggle='tooltip' title='刷新页面后可再次编辑此项' class='tooltip_th'>"+name+"</button>"+script)    
				}
			}
        });
	   
	    $('#'+id).on('blur',".input_add_teacher",function (){     
           var name;
		   name = $(this).val();
		   if (name ==''){	
		    	$(this).parent().html(html);
		   }
        });
	});
	
    
	$('.btn_edit_attr').bind('click',function(){
        var id = $(this).parent().attr('id');     
        html = $(this).detach();       
        $('#'+id).html("<input class='input_add_attr' type='text' id='' name='teacher_attr' placeholder='必修或非必修，回车即可' autofocus>");

		$('#'+id).on('keypress', ".input_add_attr", function (e) { 
			var name;
			name = $(this).val();
			
			var key = e.which; 
			if (key == 13) {
				if (name ==''){
			
					$(this).parent().html(html);
				}else{             
					$.post('/index/', {'course_id':id, 'teacher_attr':name});
					var script;
					script = "<script>$('.click_info').on('click',function(){alert('你已经编辑过此项，刷新页面后可再次编辑')});</script>"
					$(this).parent().html("<button class='btn click_info' data-toggle='tooltip' title='刷新页面后可再次编辑此项' class='tooltip_th'>"+name+"</button>"+script)    
				}
			}
        });
	   
	    $('#'+id).on('blur',".input_add_attr",function (){     
           var name;
		   name = $(this).val();
		   if (name ==''){	
		    	$(this).parent().html(html);
		   }
        });
	});
	
	
	
    $('#avatar_btn').on('click', function(){
       if ($( "#avatar_form").is(":hidden")){
           $( "#avatar_form").show();
       } 
       else{
           $( "#avatar_form").hide();
       }
    });
    
    //Get the overview of one semester
    $('.btn_edit').bind('click', function(){
    
        var id = $(this).attr('class').split(/[ ]+/)[1]
        var attr = $(this).attr('class').split(/[ ]+/)[3];
        var num;
        var credit;
        num = 0;
        credit = 0;
        $('td.'+attr).each( function(){
        
            var credit_temp;
            credit_temp = $(this).text()-0;
            credit = credit + credit_temp;
            num = num + 1;
        })
        $('#'+id).append('<p></p>'+'<p>本学期共休:</p>'+'</br>'+'<p>'+num+'门课程</p>'+'<p>'+credit+'学分</p>');
        $(this).unbind('click');
    });
    
    //JS for index2.html
    //Add course info   
    
    if($("#first_add_course_tr").length > 0){
　　  $('#add_course_button').hide();  
　　};
    
    
    $('#change_nicname_modal').on('hidden.bs.modal', function () {
        window.location.reload();
    })
    
    // JS for the tooltips in the modal
    $('.tooltip_th').each( function(){
        
        $(this).tooltip({container:'tr'});
    });
    
    // JS for the modal, clean the form when turn off
    $('#myModal').on('hidden.bs.modal', function () {
        
        $('.must_empty').each( function(){
                
            $(this).val("");;
        });
        $('#span_modal_header').html('')
    });
    
     
    // JS for the save_course button
    $('#save_course').bind('click', function(){
        
        var grade = $("#select_grade").val(); 
        var name = $('#input_name').val();
        var teacher = $('#input_teacher').val();
        var attr = $('#input_attr').val();
        var credit = $('#input_credit').val();
        var score = $('#input_score').val();
        
        if (grade=='' || name=='' || teacher=='' || attr=='' || credit=='' || score ==''){
            
            $('#span_modal_header').html('&nbsp;&nbsp;没有填写完整，无法提交保存哦！');
        }
        else{            
            
            if (score == '0' || isNaN(score) || isNaN(credit)){               
            
                $('#span_modal_header').html('&nbsp;&nbsp;学分或成绩只填数字哦！');
            }
            else{
                
                $('#myModal').modal('hide');
                $('#add_course_button').show();
                if($("#first_add_course_tr").length > 0){
                    $('#first_add_course_tr').remove();
                };
                
                $.post('/index/', {'grade':grade, 'name':name, 'teacher':teacher, 'attr':attr, 'credit':credit, 'score':score});
           };
        };        
    });
    
    // JS for the save_and_continue button
    $('#save_and_continue').bind('click', function(){
    
        var grade = $("#select_grade").val(); 
        var name = $('#input_name').val();
        var teacher = $('#input_teacher').val();
        var attr = $('#input_attr').val();
        var credit = $('#input_credit').val();
        var score = $('#input_score').val();
        
        if (grade=='' || name=='' || teacher=='' || attr=='' || credit=='' || score ==''){
            
            $('#span_modal_header').html('&nbsp;&nbsp;没有填写完整，无法提交保存哦！');
        }
        else{           
            
            if (score == '0' || isNaN(score) || isNaN(credit)){
                
                if (isNaN(credit)){
            
                    $('#span_modal_header').html('&nbsp;&nbsp;学分只填数字哦！');
                }
                else{
                
                    $('#span_modal_header').html('&nbsp;&nbsp;成绩保留一位小数哦！');
                }  
            }
            else{
                                                 
                if($("#first_add_course_tr").length > 0){
                    $('#first_add_course_tr').remove();
                };
   
                $.post('/index/', {'grade':grade, 'name':name, 'teacher':teacher, 'attr':attr, 'credit':credit, 'score':score});                
                
                $('.must_empty').each( function(){
                
                    $(this).val("");
                });
                $('#span_modal_header').html('&nbsp;&nbsp;保存课程'+'<&nbsp;'+name+'&nbsp;>'+'成功')
           };
        };
    });
    
    // JS for the myModal_wise
    // clean the modal when turn off
    $('#myModal_wise').on('hidden.bs.modal', function () {
        
        $('#modal_table_wise_div').html('');
        $('#wise_modal_header').html('');
        window.location.reload();
    });
    
    $('#myModal').on('hidden.bs.modal', function () {
         window.location.reload();
    });
    
    $(document).on('click', '.btn.btn_edit_item', function() {
        
        var id = $(this).parent().attr('id');
        html = $(this).detach();       
        $('#'+id).html("<input class='input_add_item' type='text' id='' name='' placeholder='请输入' autofocus>");
        $('#'+id).on('blur',".input_add_item",function (){
            var content;
            content = $(this).val();
            if (content ==''){

                $(this).parent().html(html);
            }
            else{
                if ( id.indexOf('score')>=0 ){
                    
                    if( isNaN(content) || content > 100 || content < 0 ){

                            $('#wise_modal_header').html('&nbsp;&nbsp;成绩填正整数！');
                            $(this).parent().html(html);
                        
                    }
                    else{
                        $(this).parent().html(content);
                        $('#wise_modal_header').html('&nbsp;&nbsp;更改成功！');
                    }
                }
                else{   
                   $(this).parent().html(content);
                   $('#wise_modal_header').html('&nbsp;&nbsp;更改成功！');
                }            
           }
        });
    });
    
    $(document).on('click', '.btn_wise_save', function() {
        
        var string='';
        
        string = string + $(this).parent().parent().children().first().children().first().val() + ';';
        $(this).parent().parent().children().slice(1,3).each( function(){
            
            string = string + $(this).text() + ';';
        });
        string = string + $(this).parent().parent().children().eq(3).children().first().val() + ';';
        string = string + $(this).parent().parent().children().eq(4).children().first().val() + ';';
        $(this).parent().parent().children().slice(5,6).each( function(){
            
            string = string + $(this).text() + ';';
        });
        
               
        var arr = string.split(';');       
        
        if (arr[5] == '0' || isNaN(arr[5])){
            
                $('#wise_modal_header').html('&nbsp;&nbsp;成绩填正整数！');
            
        }
        else{
            
            $.post('/index/', {'string':string});
            
            if($("#first_add_course_tr").length > 0){
                $('#first_add_course_tr').remove();
            };
                
            $('#wise_modal_header').html('&nbsp;&nbsp;保存课程'+'<&nbsp;'+arr[1]+'&nbsp;>'+'成功');
            
            $(this).text('保存成功');
            $(this).attr('disabled', 'true');
       }
       
        
    });
    
    $('#wise_add_course_btn').bind('click', function(){
    
       $.get('/index/', {'wise_add': 'wise_add'}, function(data){
            $('#modal_table_wise_div').append(data);
       });
       
       $('#myModal_wise').modal('show');
       
    });
    
    // JS for value.html
    $('.choose_group').button('toggle','btn-primary');
    
	$('#check_over').on('click', function(){
		var iflike = $('input:radio[name="like_or_hate"]:checked').val();
		var naming = $('input:radio[name="naming"]:checked').val();
		var naming_way = $('input:radio[name="naming_way"]:checked').val();
		var atmosphere = $('input:radio[name="atmosphere"]:checked').val();
		var teach_way = $('input:radio[name="teach_way"]:checked').val();
		var popularity = $('input:radio[name="popularity"]:checked').val();
		var mid_test = $('input:radio[name="mid_test"]:checked').val();
		var mid_test_way = $('input:radio[name="mid_test_way"]:checked').val();
		var usual_work = $('input:radio[name="usual_work"]:checked').val();
		var final_test_way = $('input:radio[name="final_test_way"]:checked').val();
		var if_dead = $('input:radio[name="if_dead"]:checked').val(); 
		var reveal = $('input:radio[name="reveal"]:checked').val();
		
		var list = [iflike,naming,naming_way,atmosphere,teach_way,popularity,mid_test,mid_test_way,usual_work,final_test_way,if_dead,reveal]
		var n = 0
		var message = ''
		$.each(list, function (i,value) {
			if (typeof(value) == 'undefined'){
				n=n+1
				if (i==0){
					message +='      【赞\\中立\\踩】项未填\r'
				}else if (i == 1){
					message +='      【点名】项未填\r'
				}else if (i == 2){
					message +='      【点名方式】项未填\r'
				}else if (i == 3){
					message +='      【课堂气氛】项未填\r'
				}else if (i == 4){
					message +='      【上课形式】项未填\r'
				}else if (i == 5){
					message +='      【上课人气】项未填\r'
				}else if (i == 6){
					message +='      【期中考试】项未填\r'
				}else if (i == 7){
					message +='      【期中考试方式】项未填\r'
				}else if (i == 8){
					message +='      【平时作业】项未填\r'
				}else if (i == 9){
					message +='      【期末考试方式】项未填\r'
				}else if (i == 10){
					message +='      【期末考难度】项未填\r'
				}else if (i == 11){
					message +='      【是否透题】项未填\r'
				}
			}
		});
		
		var Cscore = $('#select_Cscore option:selected').text();
		var Tscore = $('#select_Tscore option:selected').text();
		var degree = $('#select_degree option:selected').text();
		
		sure_message = '您的评分项为：\r'+'      课程评分：'+Cscore+'分\r'+'      教师评分：'+Tscore+'分\r'+'      期末考难度：'+degree+'分（10分为艰难）\r\r'
		
		if (n==0){
			alert(sure_message+'如果确认这些评分无误，就可以提交了：）')
		}else if (n==1){
			alert(sure_message+'另外，发现有一项未填哦！'+message)
		}else{
			alert(sure_message+'另外，发现有'+n+'项未填：\r'+message)
		}
	});
	
    //  JS for show.html
    $(document).on('click', '.poll', function(){       
        var num = $(this).children().eq(1).children().text();
        num = parseInt(num) + 1;
        $(this).children().eq(1).children().text(num);
        $(this).parent().children().each( function(){
            $(this).removeClass('poll');
        })
        var info = $(this).children().eq(1).children().attr('id');
        alert(info);
        $.post('/eot/poll/', {'poll_info':info});       
    });
   
    if($("#error_img_mao").length > 0){
        $('#img_form').show();
        window.location.hash="#error_img_mao"
    };
    
    if($("#error_file_mao").length > 0){
        $('#file_form').show();
        window.location.hash="#error_file_mao"
    };
   
   
    $('#file_btn').on('click', function(){
       if ($( "#file_form").is(":hidden")){
           $( "#file_form").show();
           $(this).html("<span class='glyphicon glyphicon-arrow-up'></span>收起");
       } 
       else{
           $( "#file_form").hide();
           $(this).html('上传文件');
       }
    });
    
    $('#img_btn').on('click', function(){
       if ($( "#img_form").is(":hidden")){
           $( "#img_form").show();
           $(this).html("<span class='glyphicon glyphicon-arrow-up'></span>收起");
       } 
       else{
           $( "#img_form").hide();
           $(this).html('上传图片');
       }
    });
	
	$('#URP_btn').on('click', function(){
       if ($( "#URP_form").is(":hidden")){
           $( "#URP_form").show();
           $(this).html("<span class='glyphicon glyphicon-arrow-up'></span>收起");
       } 
       else{
           $( "#URP_form").hide();
           $(this).html('访问数据库，更新课程信息');
       }
    });
	
	$('#wise_btn').on('click', function(){
       if ($( "#wise_form").is(":hidden")){
           $( "#wise_form").show();
           $(this).html("<span class='glyphicon glyphicon-arrow-up'></span>收起");
       } 
       else{
           $( "#wise_form").hide();
           $(this).html('上传源代码文件，更新课程信息');
       }
    });
	
	$('#other_btn').on('click', function(){
       if ($( "#other_form").is(":hidden")){
           $( "#other_form").show();
           $(this).html("<span class='glyphicon glyphicon-arrow-up'></span>收起");
       } 
       else{
           $( "#other_form").hide();
           $(this).html('为你的学校开通智能添加课程信息服务！');
       }
    });
    
    $('#reportImg_btn').on('click', function(){
       if ($( "#reportImg_table").is(":hidden")){
           $( "#reportImg_table").show();
           $(this).html("<span class='glyphicon glyphicon-arrow-up'></span>收起");
       } 
       else{
           $( "#reportImg_table").hide();
           $(this).html('举报图片');
       }
    });
   
    // JS for store course
    $('.store').on('click', function(){
        id = $(this).attr('id');
        $.get('/eot/store/', {'eot_id':id}, function(data){
            $('#heading_baseinfo').html(data);
        });
    });
    
    // JS for delStore course
    $('.delStore').on('click', function(){
        id = $(this).attr('id');
        $.get('/eot/delStore/', {'eot_id':id}, function(data){
            $('#heading_baseinfo').html(data);
        });
    });
    
    // JS for list.html
    $('#search_btn').on('click', function(){
        if ($('#list_search_content').val() == ''){
            alert('请输入搜索内容!');
        }
        else{
            var search_string;
            search_string = $('#list_search_item').val() +';';
            search_string = search_string + $('#list_search_content').val() +';';
            search_string = search_string + $('#list_search_coursescore').val() +';';
            search_string = search_string + $('#list_search_teacherscore').val() +';';
            search_string = search_string + $('#list_search_historyscore').val() +';';           
            search_string = search_string + $('input[name="mid_test"]:checked').val()+';'; 
            search_string = search_string + $('input[name="final_test_degree"]:checked').val() +';';
            search_string = search_string + $('input[name="naming"]:checked').val() +';';
            search_string = search_string + $('input[name="usual_work"]:checked').val() +';';
            //alert(search_string);
            $.get('/eot/search/', {'search': search_string}, function(data){
                $('#eotleftdown_div').html(data);
            });
        };
    });
    
    $('.search_teacher_a').on('click', function(){
        var search_string;
        search_string = 'teacher;' + $(this).attr('id') + ';'+'1.0;'+'1.0;'+'60.0;'+';'+';'+';'+';';
        $.get('/eot/search/', {'search': search_string}, function(data){
            $('#eotleftdown_div').html(data);
        });
    });
 
 
    // JS for showcomment.html
    $('#report_eotData_btn').on('click', function(){
        var info;
        info = $(this).children().eq(0).attr('id');
        $('#report_eotData_modal').modal('hide');
        $('#report_or_not').html("<p class='text-right font-red'>本资料正在审核</p>");
        $.get('/affair/report/eotData/', {'info': info}, function(data){
            $('#report_response_div').html(data);
        });
    });
});