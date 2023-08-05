<ftl-include>
  <div>
    { responseText }
    <div ref='dados'></div>
    <div ref='prog'></div>
    <!-- <ftl-error-message></ftl-error-message> -->
  </div>

  <script>
    var self = this
    self.debug = false

    function scriptExecute(extrajavascript) {
      if (extrajavascript != undefined) {
        // Associa da self.refs.prog ao retorno do $('<script>') pois o div prog é perdido quando da atualização
        var a = $('<script>')
          .attr('type', 'text/javascript')
          .text(extrajavascript)
          .replaceAll(self.refs.prog)
          // .replaceAll(self.refs.prog)
        self.refs.prog = a
      }
    }

    const fetch = () => {
      const req = new XMLHttpRequest()

      req.responseType = 'json'

      req.onload = resp => {
        if (req.status != 200) {
          if (req.status === 403) {
            // Forbiden - Não tem permissão
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
        // obj = JSON.parse(req.responseText);
        self.trigger('updateContent', req.response)
        self.trigger('loaded')
      }

      req.open('get', opts.include.url, true)
      req.setRequestHeader("X-Requested-With", "XMLHttpRequest")
      req.setRequestHeader("X-CSRFToken", getCookie('csrftoken')) //csrftoken);
      req.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken')) //csrftoken);
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

      if (opts.include.showLoading) // Se habilitado mostra janela com mensagem de carregando
        document.getElementById('commonLoad').style.display = "block";
    })

    self.on('loaded', (data) => {
      if (self.debug) console.log('ftl-include: loaded')

      document.getElementById('ftl-page-load').value='loaded';

      if (opts.include.showLoading)
        document.getElementById('commonLoad').style.display = "none";

      // Não seria melhor usar
      // if (typeof data !== 'undefined' && data !== null) {
      // Em vez de
      // if (data != undefined) {
      if (typeof data !== 'undefined' && data !== null) {
        if (data.form_errors != undefined || data.formset_errors != undefined) {
          $('input[name="save"]').show(); // Mostra campos de save se houve algum erro na validação
        }
      }
    })

    self.on('updateContent', (obj) => {
      if (opts.include.safe) self.refs.dados.innerHTML = obj.html
      else self.responseText = obj.html

      scriptExecute(obj.extrajavascript)

//      if (obj.script) {
//        // Associa da self.refs.prog ao retorno do $('<script>') pois o div prog é perdido quando da atualização
//        var a = $('<script>')
//          .attr('type', 'text/javascript')
//          .text(obj.script)
//          .replaceAll(self.refs.prog)
//          // .replaceAll(self.refs.prog)
//        self.refs.prog = a
//      }

      $(self.refs.dados).find('form:not([ref="modalForm"])').each(function() { // Exclui forms modais. Ex.: edição de conta no plano contábil
        $(this).attr('action', opts.include.url + (opts.include.url.endsWith('/') ? '' : '/'));
        $('<input>').attr({type: 'hidden', name: 'csrfmiddlewaretoken', value: getCookie('csrftoken')}).appendTo(this);
        // $(this).append
        // var that = $(this); // define context and reference
        /* for each of the submit-inputs - in each of the forms on the page - assign click and keypress event */
        // $("input:submit", that).bind("click keypress", function () {
        //     // Identifica o botão que foi efetivamente clicked. Será usado quando houver o submit para identificar que botão foi selecionado
        //     that.data("submitClickedName", this.name);
        // });
        $(this).submit(function(e) {
          // e.preventDefault()

          // var submitClickedName = $(this).data("submitClickedName")
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
              // if (self.debug) console.log('variavel=',csrftoken,' function=',getCookie('csrftoken'))
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')) //csrftoken);
              xhr.setRequestHeader("HTTP_X_CSRFTOKEN", getCookie('csrftoken')) //csrftoken);
              // xhr.setRequestHeader("Authorization", 'Token ' + token) // var token = '{{ token }}' ==> definido em base.html
              self.trigger('loading')
            },
            success: function (data) {
              if ((data.form_errors !== undefined && data.form_errors !== null) ||
                  (data.formset_errors !== undefined && data.formset_errors !== null)) {
                self.trigger('updateContent', data) // data = req.response
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
  </script>
</ftl-include>

