 /* jshint esversion: 6 */

 document.addEventListener('DOMContentLoaded', function () {
     const deleteModal = document.getElementById('deleteModal');
     if (deleteModal) {
         deleteModal.addEventListener('show.bs.modal', function (event) {
             const button = event.relatedTarget;
             const href = button.getAttribute('data-href');
             const confirmForm = document.getElementById('deleteConfirmForm');
             if (confirmForm) {
                 confirmForm.setAttribute('action', href);
             }
         });
     }
 });