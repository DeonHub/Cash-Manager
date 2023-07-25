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
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}


const downFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
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
        const paid = document.getElementById('paid')
        
        const input = document.getElementById('input')
        const total_amount_due = document.getElementById('total_amount_due')

        const amount_paid = document.getElementById('amount_paid')
        const arrears = document.getElementById('arrears')
        const charge = document.getElementById('charge')

        const balance = document.getElementById('balance')

        let charge_percentage = document.getElementById('charge_percentage')


        let payments = document.getElementById('payments')
        
        // let charge = document.getElementById('charge')





        if(event.value != ""){
                payments.style.display = "block"

                if(event.value == "part"){
        
                        // alert("Human")
                        label.style.display = "block"
                        // form_check.style.display = "block"
                        input.style.display = "block"
                        // arrears.style.display = null
                        //paid.value = 0
                        total_amount_due.value = null
        
                        paid.value = ""
                        amount_paid.value = ""
                        arrears.value = ""
                        charge.value = ""
        
                }else if(event.value == "full"){
                        label.style.display = "none"
                        // form_check.style.display = "none"
                        input.style.display = "none"
                        
        
                        total_amount_due.value = parseInt(expiration_bill.value)
                        
                        paid.value = parseInt(total_amount_due.value) - parseInt(balance.value)
        
                        amount_paid.value = paid.value
                      
                        arrears.value = 0
                        var number = parseFloat(amount_paid.value) * parseFloat(charge_percentage.value * 0.01)
                        charge.value = number.toFixed(2)
        
                        // charge.value = parseFloat(amount_paid.value) * parseFloat(charge_percentage.value * 0.01)
                        // arrears.style.display = "none"
                }else{
                        label.style.display = "none"
                        // form_check.style.display = "none"
                        input.style.display = "none"
        
                        // total_amount_due.value = parseInt(expiration_bill.value)
                        // arrears.style.display = "none"
        
                        paid.value = ""
                        total_amount_due.value = ""
                        //balance.value = ""
                        amount_paid.value = ""
                        arrears.value = ""
                        charge.value = ""
        
                }
        
        }else{
                payments.style.display = "none"
        }
     


}




const decreaseCounter = () => {
        const decrease = document.getElementById('pre').value
        parseInt(decrease)++
       alert(decrease)
 }


const memberOut = () => {
        // alert("Hello")
        window.localStorage.removeItem('token');
    }
    


const getFile = () => {

        const signature = document.getElementById('signature')
        const signaturePreview = document.getElementById('signature-preview')
        const previewImage = document.querySelector(".image")
        const previewTextDefault = document.querySelector(".default-text")

        signature.addEventListener('change', function() {
                const file = this.files[0];
                
        
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        signaturePreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        signaturePreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}


const getLogo = () => {

        const logo = document.getElementById('logo')
        const logoPreview = document.getElementById('logo-preview')
        const previewImage = document.querySelector(".logo-image")
        const previewTextDefault = document.querySelector(".logo-text")

        logo.addEventListener('change', function() {
                const file = this.files[0];
                
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        logoPreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        logoPreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
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
        let payment_status = document.getElementById('payment_status')
        let invoice_type = document.getElementById('invoice_type')

        let charge_percentage = document.getElementById('charge_percentage')
        let charge = document.getElementById('charge')
        


        if(invoice_type.value  == "expiry"){
                if(payment_status.value == "part"){

                        // alert("Amount paid should not be less than amount due")
                        
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
                        }else{
                                alert("Amount paid should not be less than amount due")
                                amount.value = ""       
                                arrears.value = ""       
                        }
                }
                else if(payment_status.value == "full"){
                        if(parseInt(amount.value) < parseInt(paid.value)){
                                alert("Amount paid should not be less than amount due")
                                amount.value = ""
                                arrears.value = "" 
                        }else{
                                arrears.value = 0 
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
                                arrears.value = "" 
                        } 
                        else{
                                arrears.value = 0
                        }
                }

                else if (payment_status.value == "part"){
                        if(parseInt(amount.value) >= parseInt(paid.value)){
                                
                                arrears.value = parseInt(outstanding_bill.value) - parseInt(amount.value)
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
        }




        if(amount.value == ""){
                charge.value = ""
        }
        else{
                var number = parseFloat(amount.value) * parseFloat(charge_percentage.value * 0.01)
                charge.value = number.toFixed(2)
        }
     

  
}


const disbleMembers = (event) => {
        let members = document.getElementById("member")

        event.checked ? members.disabled = true : members.disabled = false


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



const allBranches = (event) => {
        let branch = document.getElementById("branch")
        let all_groups = document.getElementById("all_groups")
        let all_subgroups = document.getElementById("all_subgroups")
        let all_groups_check = document.getElementById("all_groups_check")
        let all_subgroups_check = document.getElementById("all_subgroups_check")

        event.checked ? branch.disabled = true : branch.disabled = false
        event.checked ? all_groups.disabled = true : all_groups.disabled = false
        event.checked ? all_subgroups.disabled = true : all_subgroups.disabled = false
        event.checked ? all_groups_check.disabled = true : all_groups_check.disabled = false
        event.checked ? all_subgroups_check.disabled = true : all_subgroups_check.disabled = false
        
}

const allGroups = (event) => {
        let all_groups = document.getElementById("all_groups")
        let all_subgroups = document.getElementById("all_subgroups")
        let all_subgroups_check = document.getElementById("all_subgroups_check")

        event.checked ? all_groups.disabled = true : all_groups.disabled = false
        event.checked ? all_subgroups.disabled = true : all_subgroups.disabled = false
        event.checked ? all_subgroups_check.disabled = true : all_subgroups_check.disabled = false
        
}

const allSubgroups = (event) => {
        let all_subgroups = document.getElementById("all_subgroups")
        event.checked ? all_subgroups.disabled = true : all_subgroups.disabled = false
        
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





const radioCheck = (event) => {


        
        // let radio = document.getElementById("install")
        let period = document.getElementById("period")
        let set_date = document.getElementById("set_pay_date")
        let start_date = document.getElementById("start_date")
        let end_date = document.getElementById("end_date")
        

        if(event.checked){
    

                if(event.value == "Month(s)"){
                        start_date.style.display = 'block' 
                        end_date.style.display = 'block'
                        set_date.style.display = 'none' 
                        period.style.display = 'none'   

                }


                if(event.value == "Day(s)"){
                        start_date.style.display = 'none' 
                        end_date.style.display = 'none' 
                        set_date.style.display = 'block' 
                        period.style.display = 'none'         
                }





                if(event.value == "Year(s)"){
                        period.style.display = 'block'         
                        period.placeholder = `Enter no. of years eg, 1 or 2 or 3` 
                        set_date.style.display = 'none' 
                        start_date.style.display = 'none' 
                        end_date.style.display = 'none' 
                }
                                                        
        }
                // }
} 






const radioCheck2 = (event) => {

        let period = document.getElementById("numver")

        period.placeholder = `Enter the number of ${event.value} to renew for...`
        period.disabled = false    

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






// const getValue = () => {
//         $('#{values}').on("change", function() {

//                 $('.data').each(function() {
//                   alert($(this).val())
                 
//                 });
                
//               });
//                 $(".data").on("change", function() {
              
//                 $('.data').each(function() {
//                   alert($(this).val())
                 
//                 });
                
//               }); 
// }
//         // $(document).ready(function(){
        //         $("button").click(function(){
        //           $("p").slideToggle();
        //         });
        //       });

//                 // Fee Items
// $("#fee_type").change(function () {
//                 var url = $("#myFormID").attr("data-items-url");
//                 var fee_type = $(this).val();
            
//                 $.ajax({
//                   url: url,
//                   data: {
//                     'fee_type': fee_type,
//                   },
//                   success: function (data) {
//                     $("#fee_items").html(data);
//                   }
//                 });
            
//         });  
        


function pullDisc(source){
        disc = document.getElementById('disc')

        if (source.checked == true){
                disc.style.display = 'block';
        }
        else{
                disc.style.display = 'none';
        }
}




const checkDiscount = () => {

        let total = document.getElementById('total')
        let discounted_amount = document.getElementById('discounted_amount')
        let discount = document.getElementById('discount')

        if(discount.value == "" || parseInt(discount.value) > 100 ){
                discounted_amount.value = 0
        }else if(parseInt(discount.value) < 0){
                discounted_amount.value = parseInt(total.value)
        }
        else{
                discounted_amount.value = parseInt(total.value) - (parseFloat(total.value) * (parseFloat(discount.value) * 0.01))
        } 



}
       