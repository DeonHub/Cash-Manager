

if ('serviceWorker' in navigator) {

    window.addEventListener('load', () => {

        // C:\Users\DELL\Desktop\Fee_Sys\fee_sys\fee_sys\service_worker\service_worker.js
        navigator.serviceWorker.register("/service-worker.js", { scope: "/" }).then(registration => {

            console.log('SW registered: ', registration);

        }).catch(registrationError => {

            console.log('SW registration has failed: ', registrationError);

        });

    });

}