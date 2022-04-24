/* Description: Custom JS for Search Functions */
$(function () {
        function showTrack(released) {
            document.getElementById("player").src = "https://stream.resonate.coop/embed/track/" + released;
            document.getElementById("listen").href = "https://stream.resonate.coop/track/" + released;

        }
        function search() {
            const query = $("#search").find("input[name=search]").val();
            $.get("/search?q=" + encodeURIComponent(query),
                function (data) {
                    const t = $("table#results tbody").empty();
                    if (!data || data.length == 0) return;
                    data.forEach(function (track) {
                        $("<tr><td class='track'>" + track.title + "</td><td>" + track.tagline + "</td></tr>"
                        ).appendTo(t)
                            .click(function () { showTrack(track.released); })

                    });
                    showTrack(data[0].released);
                }, "json");
            return false;
        }

        $("#search").submit(search);
        search();

        function search1() {
            const query = $("#search").find("input[name=search]").val();
            $.get("/suggested_search?q=" + encodeURIComponent(query),
                function (data) {
                    const t = $("table#results2 tbody").empty();
                    if (!data || data.length == 0) return;
                    data.forEach(function (track) {
                        $("<tr><td class='track'>" + track.title + "</td><td>" + track.tagline + "</td></tr>"
                        ).appendTo(t)
                            .click(function () { showTrack(track.released); })

                    });
                    showTrack(data[0].released);
                }, "json");
            return false;
        }

        $("#search").submit(search1);
        search1();

    })