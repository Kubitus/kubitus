$(function () {
    $("dl.accordion").each(function () {
        var $dl = $(this);
        $dl
            .find("dd")
            .hide();
        $dl
            .find("dt")
            .click(function () {
                var $dt = $(this),
                    $dd = $dt.next("dd");
                if($dd.is(":not(:visible)")) {
                    $dl
                        .find("dd:visible")
                        .slideUp();
                    $dd
                        .slideDown();
                } else {
                    $dd.slideUp();
                }
            });
    });
});
