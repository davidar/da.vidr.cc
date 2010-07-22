google.load("feeds", "1");

function date2iso8601(date) {
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    if(month < 10) {
        month = '0' + month;
    }
    var day = date.getDate();
    if(day < 10) {
        day = '0' + day;
    }
    return year + '-' + month + '-' + day;
}

$(document).ready(function() {
    var feed = new google.feeds.Feed("http://github.com/davidar/da.vidr.cc/commits/master.atom");
    feed.setNumEntries(10);
    feed.load(function(result) {
        if(!result.error) {
            var container = $('<ul>');
            $('#changelog-feed').append(container);
            for(var i = 0; i < result.feed.entries.length; i++) {
                var entry = result.feed.entries[i];
                container.append($('<li>').text(date2iso8601(new Date(entry.publishedDate)) + ': ' + entry.title));
            }
        }
    });
});
