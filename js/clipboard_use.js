!function (e, t, a) {
    var initCopyCode = function () {
        var copyHtml = '';
        copyHtml += '<button class="btn-copy" data-clipboard-snippet="">';
        copyHtml += '<i class="fa fa-clipboard"></i>';
        copyHtml += '</button>';
        $("figure.highlight table").before(copyHtml);

        var clipboard = new ClipboardJS('.btn-copy', {
                target: function (trigger) {
                    var table = trigger.nextElementSibling.firstElementChild;
                    return table.firstElementChild.firstElementChild.firstElementChild.nextElementSibling;
                }
        });

        clipboard.on('success', function (e) {
            e.trigger.innerHTML = "<span>Done</span>"
            setTimeout(function () {
                    e.trigger.innerHTML = "<i class='fa fa-clipboard'></i>"
                }, 1000)

            e.clearSelection();
        });

        clipboard.on('error', function (e) {
            e.trigger.innerHTML = "<span>Failed</span>"
            setTimeout(function () {
                    e.trigger.innerHTML = "<i class='fa fa-clipboard'></i>"
                }, 1000)
            e.clearSelection();
        });
    }
    initCopyCode();
}(window, document);
