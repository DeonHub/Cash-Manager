// window.onload = function() {
//         let things = document.getElementsByTagName("input")
//         const inputs = Array.from(things)
//         inputs.forEach(input => {
//                 input.addEventListener('keypress', () => {
//                        if(input.readOnly == true){
//                                alert("This is a readonly field")
//                        }
//                 })
//         })
//       };



const upFile = (event) => {
    const attach_audio = document.getElementById('attach_audio')
    const voice = document.getElementById('voice')


    if(event.value == "web"){
            attach_audio.innerHTML = "Attach File"
    }else if(event.value == "audio"){
            attach_audio.innerHTML = "Attach Audio"
    }

}


const downFile = (event) => {
    const attach_audio = document.getElementById('attach_audio')
    const voice = document.getElementById('voice')


    if(event.value == "web"){
            attach_audio.innerHTML = "Attach File"
    }else if(event.value == "audio"){
            attach_audio.innerHTML = "Attach Audio"
    }

}


const checkOut = (event) => {
    const expire = document.getElementById('expire')

    if(event.checked == false){
            expire.style.display = "block"
    }
    else{
            expire.style.display = "none"
    }
    
}


const loadDuration = (event) => {
    const label = document.getElementById('label')
    const form_check = document.getElementById('form_check')
    const input = document.getElementById('input')
    const total_amount_due = document.getElementById('total_amount_due')
    const outstanding_bill = document.getElementById('outstanding_bill')
    const arrears = document.getElementById('arr')
 

    if (event.value == "part"){
            label.style.display = "block"
            form_check.style.display = "block"
            input.style.display = "block"
            arrears.style.display = null
            total_amount_due.value = null
    }else{
            label.style.display = "none"
            form_check.style.display = "none"
            input.style.display = "none"

            total_amount_due.value = parseInt(outstanding_bill.value)
            arrears.style.display = "none"
    }


}



const memberOut = () => {
    // alert("Hello")
    window.localStorage.removeItem('token');
}




const checkBill = () => {
    let bill = document.getElementById('total')
    let amount = document.getElementById('amount')

    if(parseInt(amount.value) > parseInt(bill.value)){
            alert("Installment amount should not be greater than total invoice")
            amount.value = ""
    }
}


function toggle(source) {
    checkboxes = document.getElementsByName('foo[]');
    for(var i=0, n=checkboxes.length;i<n;i++) {
      checkboxes[i].checked = source.checked;
    }
  }



const loadTotal = () => {
    let outstanding_bill = document.getElementById('outstanding_bill')
    let amount = document.getElementById('total_amount_due')
    let expiration_bill = document.getElementById('expiration_bill')
    let renewal_bill = document.getElementById('renewal_bill')

    var testExp = !!document.getElementById("expiration_bill");
    var testRen = !!document.getElementById("renewal_bill");        

    if(testExp === true && testRen === true ){
           if(parseInt(outstanding_bill.value) <= 0){
            amount.value = expiration_bill.value
           }else{
            amount.value = parseInt(expiration_bill.value) + parseInt(renewal_bill.value)       
           }
    }else{
            amount.value = parseInt(outstanding_bill.value)
    }
}



const findArrears = () => {
    let outstanding_bill = document.getElementById('outstanding_bill')
    let amount = document.getElementById('amount_paid')
    let arrears = document.getElementById('arrears')
    let expiration_bill = document.getElementById('expiration_bill')
    let total_amount_due = document.getElementById('total_amount_due')
    let paid = document.getElementById('paid')
    const payment_status = document.getElementById('payment_status')
    const user_type = document.getElementById('user_type')

//     alert(outstanding_bill)


    if (user_type.value  == "Subscriber"){
            if (payment_status.value == "part"){
                    if(parseInt(amount.value) >= parseInt(paid.value)){
    
                               if(parseInt(expiration_bill.value) > 0){
                                    arrears.value = parseInt(expiration_bill.value) - parseInt(amount.value)
                                    if(arrears.value < 0){
                                            arrears.value = 0    
                                    }
                                }
                                else{
                                    arrears.value = parseInt(outstanding_bill.value) - parseInt(amount.value)
                                    if(arrears.value < 0){
                                            arrears.value = 0    
                                    }
                                }
                    }
                   else{
                    alert("Amount paid should not be less than amount due")
                    amount.value = ""       
                    }
            }
            else if (payment_status.value == "full"){
                    if(parseInt(amount.value) < parseInt(paid.value)){
                            alert("Amount paid should not be less than amount due")
                            amount.value = ""
                    } 
            }else{
                    alert("Please select a payment status")
                    amount.value = ""
            }
    }else{
            if (payment_status.value == "full"){
                    if(parseInt(amount.value) < parseInt(paid.value)){
                            alert("Amount paid should not be less than amount due")
                            amount.value = ""
                    } 
                    else{
                            arrears.value = 0
                    }
            }

            else if (payment_status.value == "part"){
                    if(parseInt(amount.value) >= parseInt(paid.value)){
                            
                            arrears.value = parseInt(total_amount_due.value) - parseInt(amount.value)
                            if(arrears.value < 0){
                                    arrears.value = 0    
                            }
                                
                    }
                      else{

                            arrears.value = parseInt(total_amount_due.value) - parseInt(amount.value)
                            if(arrears.value < 0){
                                    arrears.value = 0    
                            }
                            
                            
                                

                    }
            }  
    }
 


}


const disbleMembers = (event) => {
    let members = document.getElementById("member")

    if (event.checked == true) {
            members.disabled = true
    } else {
            members.disabled = false
        }



}




const disbleDonor = (event) => {
    let donor_name = document.getElementById("donor_name")
    let donor_contact = document.getElementById("donor_contact")
    let donor_email = document.getElementById("donor_email")
    let countries = document.getElementById("countries")
    let para = document.getElementById("para")

    if (event.checked == true) {
            countries.disabled = true
            donor_name.disabled = true
            donor_contact.disabled = true
            donor_email.disabled = true
            para.style.display="block"
    } else {
            donor_name.disabled = false
            donor_contact.disabled = false
            donor_email.disabled = false
            countries.disabled = false
            para.style.display="none"

        }



}




const checkFunction = () => {
    for(let i=1; i<10; i++){
                let checkBox = document.getElementById("fee_type"+i)
                let amount = document.getElementById("item_amount"+i)

        if (checkBox.checked == true) {
                amount.style.display = "block"
        } else {
                amount.style.display = "none";
            }
        }
    }



const radioCheck = () => {
    for(let i=1; i<5; i++){
            let radio = document.getElementById("install"+i)
            let period = document.getElementById("period")
            let set_date =   document.getElementById("set_pay_date")

            if(radio.checked){
                    amount.disabled = false 

                    if(radio.value == "None"){
                            period.disabled = true    
                            set_date.disabled = false 

                    }
                    else{
                            period.placeholder = `Enter the number of ${radio.value}` 
                            period.disabled = false    
                            set_date.disabled = true       
                    }
            }
            }
} 

const radioCheck2 = () => {
    for(let i=1; i<5; i++){
            let radio = document.getElementById("range"+i)
            let period = document.getElementById("numver")

            if(radio.checked){
                    period.placeholder = `Enter the number of ${radio.value} to renew for...`
                    period.disabled = false    
            }
            }
}


const checkDate = () => {

    let check = document.getElementById('check')

    if(check.checked == true){
            document.getElementById("start_date").disabled = false
            document.getElementById("end_date").disabled = false
    }else{
            document.getElementById("start_date").disabled = true
            document.getElementById("end_date").disabled = true 
    }
}






   