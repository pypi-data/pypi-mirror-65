riot.tag2('ftl-timeout', '<span></span>', '', '', function(opts) {
  var self = this;
  self.delay = 5*60*1000
  self.inc = undefined
  self.url = undefined
  self.responseText = undefined

  self.on('mount', () => {
    self.url = opts.url
    self.trigger('updateContent')
  })
  self.on('updateContent', () => {

    const req = new XMLHttpRequest()
    req.responseType = 'json'
    req.onload = resp => {
      if (req.status != 200) {

      } else {

        this.root.innerHTML = req.response.html
        self.update()
      }
      setTimeout(function() {
        self.trigger('updateContent')
      }, self.delay);
    }

    req.open('get', self.url, true)
    req.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    req.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
    req.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken'))
    req.send()
  })
});
