 /* jshint esversion: 6 */

 document.addEventListener('DOMContentLoaded', function () {
     const firmInput = document.getElementById('firm-input');
     const slugInput = document.getElementById('slug-input');

     firmInput.addEventListener('input', function () {
         const slugified = firmInput.value
             .toLowerCase()
             .replace(/[^a-z0-9]+/g, '-')
             .replace(/^-+|-+$/g, '');
         slugInput.value = slugified;
     });
 });