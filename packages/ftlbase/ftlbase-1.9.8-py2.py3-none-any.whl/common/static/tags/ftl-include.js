riot.tag2('ftl-include', '<div> {responseText} <div ref="dados"></div> <div ref="prog"></div> </div>', '', '', function(opts) {
    var self = this
    self.debug = false

    function scriptExecute(extrajavascript) {
      if (extrajavascript != undefined) {

        var a = $('<script>')
          .attr('type', 'text/javascript')
          .text(extrajavascript)
          .replaceAll(self.refs.prog)

        self.refs.prog = a
      }
    }

    const fetch = () => {
      const req = new XMLHttpRequest()

      req.responseType = 'json'

      req.onload = resp => {
        if (req.status != 200) {
          if (req.status === 403) {

            alert('Desculpe, mas você não tem permissão!')
            window.history.back()
          } else if ((req.status === 500) && (req.responseURL !== undefined)) {
            window.location = req.responseURL;
          }
          else
            alert('Request failed.  Returned status of ' + req.status);
        }
        if (req.response == undefined) {
          if (req.responseURL.indexOf("/common/login/?next=") !== -1) {
            window.location = req.responseURL;
          }
          return;
        }

        self.trigger('updateContent', req.response)
        self.trigger('loaded')
      }

      req.open('get', opts.include.url, true)
      req.setRequestHeader("X-Requested-With", "XMLHttpRequest")
      req.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
      req.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken'))
      req.send()
      self.trigger('loading')
    }

    self.on('mount', () => {
      if (self.debug) console.log('ftl-include: mount:', opts.include.url)
      fetch()
    })

    self.on('loading', () => {
      if (self.debug) console.log('ftl-include: loading')

      document.getElementById('ftl-page-load').value='loading';

      if (opts.include.showLoading)
        document.getElementById('commonLoad').style.display = "block";
    })

    self.on('loaded', (data) => {
      if (self.debug) console.log('ftl-include: loaded')

      document.getElementById('ftl-page-load').value='loaded';

      if (opts.include.showLoading)
        document.getElementById('commonLoad').style.display = "none";

      if (typeof data !== 'undefined' && data !== null) {
        if (data.form_errors != undefined || data.formset_errors != undefined) {
          $('input[name="save"]').show();
        }
      }
    })

    self.on('updateContent', (obj) => {
      if (opts.include.safe) self.refs.dados.innerHTML = obj.html
      else self.responseText = obj.html

      scriptExecute(obj.extrajavascript)

      $(self.refs.dados).find('form:not([ref="modalForm"])').each(function() {
        $(this).attr('action', opts.include.url + (opts.include.url.endsWith('/') ? '' : '/'));
        $('<input>').attr({type: 'hidden', name: 'csrfmiddlewaretoken', value: getCookie('csrftoken')}).appendTo(this);

        $(this).submit(function(e) {

          var submitClickedName = $(document.activeElement)[0].name
          var submitClickedValue = $(document.activeElement)[0].value

          if ($(document.activeElement)[0].type === 'checkbox') {
            submitClickedValue = $(document.activeElement)[0].checked
          }

          $(":disabled").removeProp('disabled')

          document.activeElement.disabled=true;

          $f = $(this)
          var type = $f.attr('method')
          var dados = $f.serialize() + '&'+submitClickedName+'='+ submitClickedValue
          var url = $f.attr('action')
          $.ajax({
            type: type,
            url: url,
            data: dados,
            xhrFields: {
              withCredentials: true
            },
            beforeSend:function(xhr, settings) {

              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
              xhr.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken'))

              self.trigger('loading')
            },
            success: function (data) {
              if ((data.form_errors !== undefined && data.form_errors !== null) ||
                  (data.formset_errors !== undefined && data.formset_errors !== null)) {
                self.trigger('updateContent', data)
              } else if (data.goto != undefined) {
                eval(data.extrajavascript);
                route('/'+data.goto)
              } else if (self.debug) console.log("OK: ---\>"+data+"\<---")
              if (data.msg != undefined) {
                if (self.debug) console.log(data.msg)
                riot.mount('ftl-error-message', { messages: data.msg })
              }
              self.trigger('loaded', data)
              return false;
            },
            error: function( xhr, status, error) {
              if (self.debug) console.log("Something went wrong: >"+xhr+"< >"+status+'< >'+error+'<');
              document.open();
              document.write(xhr.responseText);
              document.close();
              return false;
            }
          });
          return false;
        });
      })

      self.update()
    })
});

