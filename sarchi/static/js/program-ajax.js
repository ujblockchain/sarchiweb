dormElement={
    'firstName': document.getElementById('id_first_name'),
    'lastName': document.getElementById('id_last_name'),
    'gender': document.getElementById('id_gender'),
    'email': document.getElementById('id_email'),
    'nationality': document.getElementById('id_nationality'),
    'phoneNumber': document.getElementById('id_phone_number'),
    'expectation': document.getElementById('id_expectation'),
    'submitBtn': document.getElementById('btn_submit'),
    'formAlert': document.querySelector('.success-msg'),
    'formAlertIcon': document.querySelector('.fa-paper-plane-o'),
}

//init form data object
const formData = new FormData();

//set post link
const formActionLink='/event/registration/';

//get csrf token
const csrf = document.getElementsByName('csrfmiddlewaretoken');

//append form csrf to form data object
formData.append('csrfmiddlewaretoken', csrf[0].value);


dormElement.submitBtn.addEventListener('click', (e) => {
    e.preventDefault();

    //append data to form data object
    formData.append('first_name', dormElement.firstName.value);
    formData.append('last_name', dormElement.lastName.value);
    formData.append('gender', dormElement.gender.value);
    formData.append('email', dormElement.email.value);
    formData.append('nationality', dormElement.nationality.value);
    formData.append('expectation', dormElement.expectation.value);
    formData.append('phone_number', dormElement.phoneNumber.value);
    
    $.ajax({
        type:'POST',
        url: formActionLink,
        data: formData,
        beforeSend: function(){

            console.log('before send');

            // reset alert
            dormElement.formAlert.style.display = 'none';
            dormElement.formAlertIcon.style.border= 'none';

            //disable submit btn.
            dormElement.submitBtn.style.pointerEvents = 'none'
            dormElement.submitBtn.textContent = 'Processing ...'
            dormElement.submitBtn.classList.add('btn_ajax')
        },
        xhr: function(response){

            const xhr = new window.XMLHttpRequest();
            let percent; 
            xhr.upload.addEventListener('progress', e =>{

                //calculate percentage
                percent = e.loaded / e.total * 100;
                
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

                    //reset all input error
                    let inputs = document.querySelectorAll('input')
                    Array.from(inputs).forEach((input) => {
                        input.style.border = 'none';
                    })

                    //reset all select
                    let select_field = document.querySelectorAll('select')
                    Array.from(select_field).forEach((select) => {
                        select.style.border = 'none';
                    })

                    //reset text area
                    let textarea_field = document.querySelector('textarea')
                    textarea_field.style.border = 'none';
                })
                        
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
                dormElement.gender.value = 'Gender';
                dormElement.email.value = '';
                dormElement.nationality.value = 'Select Nationality';
                dormElement.expectation.value = '';
                dormElement.phoneNumber.value = '';

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
                    let select_field = document.querySelectorAll('select')
                    Array.from(select_field).forEach((select) => {
                        select.style.border = 'none';
                    })

                    //reset text area
                    let textarea_field = document.querySelector('textarea')
                    textarea_field.style.border = 'none';
                })
            }

            //reset submit btn as long there is a response.
            dormElement.submitBtn.style.pointerEvents = 'all'
            dormElement.submitBtn.textContent = 'SUBMIT'
            dormElement.submitBtn.classList.remove('btn_ajax')

        },
        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})