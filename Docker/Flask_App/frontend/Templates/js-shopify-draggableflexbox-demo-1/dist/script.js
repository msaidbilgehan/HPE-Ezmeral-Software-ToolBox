/* https://shopify.github.io/draggable/examples/flexbox.html
 */

/* Source: https://codepen.io/tommyho tommyho510@gmail.com */

/* To apply this applet to your website, paste the following code into your code:

<iframe style="width: 400px; height: 400px;" src="https://codepen.io/tommyho/full/RweEqoN"></iframe>

*/

$(document).ready(function () {
  var sortable = new Draggable.Sortable(document.querySelectorAll(".menu"), {
    draggable: ".submenu",
    handle: ".submenu_handle",
    swapAnimation: {
      duration: 200,
      easingFunction: "ease-in-out",
      vertical: true
    },
    plugins: [Draggable.Plugins.SwapAnimation]
  });
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});