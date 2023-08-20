dormElement={
    'firstName': document.getElementById('id_first_name'),
    'lastName': document.getElementById('id_last_name'),
    'email': document.getElementById('id_email'),
    'faculty': document.getElementById('id_faculty'),
    'department': document.getElementById('id_department'),
    'level': document.getElementById('id_level'),
    'expectation': document.getElementById('id_expectation'),
    'submitBtn': document.getElementById('btn_submit'),
    'formAlert': document.querySelector('.success-msg'),
    'formAlertIcon': document.querySelector('.fa-paper-plane-o'),
}

//init form data object
const formData = new FormData();

//set post link
const formActionLink='/bootcamp/registration';

//get csrf token
const csrf = document.getElementsByName('csrfmiddlewaretoken');

//append form csrf to form data object
formData.append('csrfmiddlewaretoken', csrf[0].value);


dormElement.submitBtn.addEventListener('click', (e) => {
    e.preventDefault();

    //append data to form data object
    formData.append('first_name', dormElement.firstName.value);
    formData.append('last_name', dormElement.lastName.value);
    formData.append('email', dormElement.email.value);
    formData.append('faculty', dormElement.faculty.value);
    formData.append('department', dormElement.department.value);
    formData.append('level', dormElement.level.value);
    formData.append('expectation', dormElement.expectation.value);
    
    $.ajax({
        type:'POST',
        url: formActionLink,
        data: formData,
        beforeSend: function(){

            console.log('before send');

            // reset alert
            dormElement.formAlert.style.display = 'none';
            dormElement.formAlertIcon.style.border= 'none';
        },
        xhr: function(response){

            const xhr = new window.XMLHttpRequest();
            let percent; 
            xhr.upload.addEventListener('progress', e =>{

                //calculate percentage
                percent = e.loaded / e.total * 100;

                //log progress
                console.log(percent)
                
            })
            
            return xhr
        },
        success: function(response){
            //loop through error
            if(response.error){
                //reset all error fields firsts
                Array.from(document.querySelectorAll('.error-info')).forEach((field) => {
                    //set empty content
                    field.textContent = '';

                    //ensure error display is none
                    field.style.display = 'none';

                    // remove error border
                    field.previousElementSibling.style.border = 'none';

                    //reset all input error
                    let inputs = document.querySelectorAll('input')
                    Array.from(inputs).forEach((input) => {
                        input.style.border = 'none';
                    })

                    //reset all select
                    document.querySelector('select').style.border = 'none';
                })
                
                console.log(response.message)
        
                //loop through error
                for (let [key, value] of Object.entries(response.error)) {
                    if(response.message == "duplicate_error"){
                        // style displayed alert
                        dormElement.formAlert.style.display = 'block';
                        dormElement.formAlert.innerHTML= `<i class="fa fa-paper-plane-o" style="border: 1px solid #ef9a9a"></i> ${response.error}`;
                    }else if(response.message == "error"){

                        //set error display text
                        document.getElementById(`error-${key}`).textContent = value[0];
                        //show error
                        document.getElementById(`error-${key}`).style.display = 'block';
                        //add error styling to input
                        document.getElementById(`error-${key}`).previousElementSibling.style.border = '1px solid #dc3545';
                        
                        // style displayed alert
                        dormElement.formAlert.style.display = 'block';
                        dormElement.formAlert.innerHTML= `<i class="fa fa-paper-plane-o" style="border: 1px solid #ef9a9a"></i> Invalid form fields`;
                    }
                }
            }else{
                //style displayed alert
                dormElement.formAlert.style.display = 'block';
                dormElement.formAlert.innerHTML= `<i class="fa fa-paper-plane-o" style="border: 1px solid #ABD0A8"></i> ${response.status}`;

                //reset form
                dormElement.firstName.value = '';
                dormElement.lastName.value = '';
                dormElement.email.value = '';
                dormElement.faculty.value = '';
                dormElement.department.value = '';
                dormElement.level.value = 'Select your level';
                dormElement.expectation.value = '';

                //reset error
                Array.from(document.querySelectorAll('.error-info')).forEach((field) => {
                    //set empty content
                    field.textContent = '';

                    //ensure error display is none
                    field.style.display = 'none';

                    //reset all input error
                    let inputs = document.querySelectorAll('input')
                    Array.from(inputs).forEach((input) => {
                        input.style.border = 'none';
                    })

                    //reset all select style
                    document.querySelector('select').style.border = 'none';
                })
            }

        },
        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})