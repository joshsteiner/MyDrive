const fsop = {
    URL: '/drive/fsop',

    ls: async function(dirID) {
        return $.ajax({
            url: fsop.URL,
            type: 'GET',
            data: { op: 'ls', dirID },
        })
    },

    mkdir: function() {},
    rmdir: function() {},
    updir: function() {},
    downdir: function() {},
    rmfile: function() {},
    upfile: function() {},
    downfile: function() {},
}