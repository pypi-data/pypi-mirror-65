// Global settings to ajax, to send CSRFTOKEN with request
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    // if (!csrfSafeMethod(settings.type) && !this.crossDomain) { // Desabilita verificação se GET para forçar autenticação
    if (!this.crossDomain) {
      csrftoken = getCookie('csrftoken');
      xhr.setRequestHeader("HTTP_X_CSRFTOKEN", csrftoken); //csrftoken);
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      // xhr.setRequestHeader("Authorization", 'Token ' + token); // var token = '{{ token }}' ==> definido em base.html
    }
  }
});

function showWorkflow(the_select, el, cls) {
  var e = document.getElementById('id_main-' + el);
  // var e = document.getElementById("elementId");
  var value, text, url;

  if (e.type === 'select-one') {
    value = e.options[e.selectedIndex].value;
    text = e.options[e.selectedIndex].text;
    url = '/' + value
  }
  ftl_modal(value, '7', '/common/workflow/process_graph/' + value + '/', text, cls);
}

function ftl_modal(pk, acao, acaoURL, modaltitle, cls) {
  if (cls === undefined)
    cls = 'modal-lg';
  ftl_modal_mount = riot.mount('div#ftl-modal', 'ftl-modal',
    {
      'modal': {isvisible: false, contextmenu: false, cls: cls},
      'data': {pk: pk, acao: acao, acaoURL: acaoURL, modaltitle: modaltitle}
    });
}

function changeUF2(the_select, valor) {
  if (the_select.selectedIndex < 0) {
    return
  }
  var uf = the_select.options[the_select.selectedIndex].value;
  //var name = the_select.name.substr(0, the_select.name.length-3);
  //var name = the_select.name.substr(0, the_select.name.length);
//    var name = 'main-municipio';

  var app_label = the_select.getAttribute('data-app_label');
  var object_name = the_select.getAttribute('data-object_name');

  var name = 'id_';
  var lastIndex = the_select.id.lastIndexOf("-");
  if (lastIndex >= 0) {
    name = the_select.id.substring(0, the_select.id.lastIndexOf("-") + 1);
  }
  var id = name + 'municipio';

  if (uf !== "") {
    // Acha o tab ativo, pois pode ter mais de um tab com id_municipio aberto
    var a = the_select.closest("div[class^='tab-pane active']");
    var b = $(a);
    // Acha o campo de select do município dentro do tab ativo
    // var mun_sel = b.find('select[id="id_municipio"]')
    var mun_sel = b.find('select[id="' + id + '"]');
    // var mun_sel = jQuery(id);
    mun_sel.attr('disabled', true).html('<option value="">Aguarde...</option>');
    mun_sel.load(
      //__municipios_base_url__+'ajax/'+uf+'/'+app_label+'/'+object_name+'/',
      '/cliente/municipio/ajax/' + uf + '/' + app_label + '/' + object_name + '/',
      null,
      function () {
        mun_sel[0].disabled = false;
        if (valor !== "") {
          $('#' + id).val(valor);
          //alert("Formato de CEP inválido.");
        }
        //alert("Formato de CEP inválido.");
      }
    );
  } else {
    jQuery(id).html('<option value="">--</option>');
  }
}

function changeUF(the_select) {
  changeUF2(the_select, "");
}

function changeCEP(the_select) {

  //Nova variável "cep" somente com dígitos.
  var cep = $(the_select).val().replace(/\D/g, '');

  //Verifica se campo cep possui valor informado.
  if (cep !== "") {

    //Expressão regular para validar o CEP.
    var validacep = /^[0-9]{8}$/;

    //Valida o formato do CEP.
    if (validacep.test(cep)) {
      var name = 'id_';
      var lastIndex = the_select.id.lastIndexOf("-");
      if (lastIndex >= 0) {
        name = the_select.id.substring(0, the_select.id.lastIndexOf("-") + 1);
      }
      // Acha o tab ativo, pois pode ter mais de um tab com id_municipio aberto
      var a = the_select.closest("div[class^='tab-pane active']");
      var b = $(a);
      // Acha o campo de input do endereço dentro do tab ativo
      var endereco = b.find('input[id="' + name + 'endereco"]');
      var bairro = b.find('input[id="' + name + 'bairro"]');
      var estado = b.find('select[id="' + name + 'estado"]');
      var municipio = b.find('select[id="' + name + 'municipio"]');
      //Preenche os campos com "..." enquanto consulta webservice.
      endereco.val("...");
      bairro.val("...");
      estado[0].value = "";
      municipio[0].value = "";

      //Consulta o webservice viacep.com.br/
      $.getJSON("//viacep.com.br/ws/" + cep + "/json/unicode/?callback=?", function (dados) {

        if (!("erro" in dados)) {
          //Atualiza os campos com os valores da consulta.
          endereco.val(dados.logradouro);
          bairro.val(dados.bairro);
          estado[0].value = dados.uf;
          changeUF2(estado[0], dados.ibge);
          municipio[0].value = dados.ibge;

        } else {
          //CEP pesquisado não foi encontrado.
          limpa_formulario_cep();
          alert("CEP não encontrado.");
        }
      });
    } //end if.
    else {
      //cep é inválido.
      limpa_formulario_cep();
      alert("Formato de CEP inválido.");
    }
  } //end if.
  else {
    //cep sem valor, limpa formulário.
    limpa_formulario_cep();
  }
}

function changeContaDestino(the_select, contaDestino) {
  // the_select é o campo de incidência que seleciona entre Proprietário, Locatário ou Administradora
  // var filtro = "";
  var id = "#id_" + contaDestino;

  var incidencia = the_select.options[the_select.selectedIndex].value;
  if (incidencia !== "") {
    var app_label = the_select.getAttribute('data-app_label');
    var object_name = the_select.getAttribute('data-object_name');

    var planodecontas = $('#planodecontas').val();
    var url = "/" + app_label + "/ajax" + object_name + "Select/" + planodecontas + "/" + incidencia + "/" + app_label + "/" + object_name + "/";

    var field_sel = jQuery(id);
    field_sel.attr('disabled', true).html('<option value="">Aguarde...</option>');
    field_sel.load(
      //__municipios_base_url__+'ajax/'+incidencia+'/'+app_label+'/'+object_name+'/',
      url,
      null,
      function () {
        field_sel[0].disabled = false;
        $(id).prepend('<option value="" selected>---------</option>');
        //$(id).val("");
        //if(valor !== ""){
        //    $(id).val(valor);
        //}
      }
    );
  } else {
    jQuery(id).html('<option value="">--</option>');
  }
  // if(incidencia !== ""){
  // }
}

function changeContaOrigemProvisao(the_select, origem, provisao) {
  changeContaDestino(the_select, origem);
  changeContaDestino(the_select, provisao);
}

function limpa_formulario_cep() {
  // Limpa valores do formulário de cep.
  $("#id_endereco").val("");
  $("#id_bairro").val("");
  //$("#id_municipio").val("");
  //$("#id_estado").val("");
}

function setHeight(jq_in) {
  // Set height of a element to fit content
  // Usado com summernote para autofit o conteúdo
  jq_in.each(function (index, elem) {
    // https://stackoverflow.com/questions/40420782/auto-resizing-textarea-in-a-modal
    elem.style.overflow = 'hidden';
    elem.style.height = 0;
    elem.style.height = `${ elem.scrollHeight + 2 }px`;

    // // This line will work with pure Javascript (taken from NicB's answer):
    // elem.style.height = elem.scrollHeight + 'px';
  });
}

// Thanks Django - to get CSRF cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

// Verifica se está em método que precisa autorização
// Não sendo usado pois todos os requests para DRF precisam de autorização
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function configuraCampos(disableMe, readonly) {
  // Busca se há formset com classe disableMe e faz o disable (inclusão de andamento)
  // if ( '{{ disableMe }}' === 'True' ) {
  var disable = $(".disableMe"); // Divs
  var disableSelect = $(".disableMe select[data-autocomplete-light-function='select2']"); // autocompletelight
  if (disableMe) {
    // Insere disable nos template de inline
    disable.removeProp('disabled');
    disable.prop('disabled', 'disabled');
    // disable.filter() => Por que estava SEM ponto e vírgula???? O que faz???
    disable.has('.has-error').removeProp('disabled');
    // Span não tem disable, então tem que usar pointer-events
    disable.filter('SPAN').css("pointer-events", "none");
    // Insere disable nos select dos autocompletelight fields
    disableSelect.removeProp('disabled');
    disableSelect.prop('disabled', 'disabled');
    // disableSelect.filter() => Por que estava SEM ponto e vírgula???? O que faz???
    disableSelect.has('.has-error').removeProp('disabled');
    // Span não tem disable, então tem que usar pointer-events
    // Insere disable nos template de inline
    // $("#detail-template").find('.disableMe').removeProp('disabled');
    // $('div[id^="detail-template"]').find('.disableMe').removeProp('disabled');
    $('div[id*=__prefix__]').find('.disableMe').removeProp('disabled');
    if (readonly) {
      $('input[name="save"]').hide();
    }
  } else {
    // $("fieldset.disableMe").removeProp('disabled');
    disable.removeProp('disabled');
  }

  // Se readonly então esconde todos os botões de adição de detalhe e o de post
  if (readonly) {
    $('a[id^="add-item-button"]').hide();
  }

  // No post, retira o disable, pois o Django só valida campos habilitados
  $("form").each(function () {
    $(this).submit(function () {
      $(":disabled").removeProp('disabled');
    });
  });
}

function configuraPagina() {
  // // Setup Django-Polymorphic for inline polymorphic formset
  $('.js-django-inlines').each(function () {
    var $this = $(this);
    var data = $this.data();

    // Local onde será feito o append das novas linhas
    // data.options.newFormTarget = ".js-django-inlines-forms";

    // A cada novo form adicionado, faz a reconfiguração da página
    data.options.onAdd = function (formset_item, options) {
      // group é o this dessa função
      // var management_form = data.djangoInline._getManagementForm();
      configuraPagina();
    };
    $this.djangoInline(data.options || data);
    // Reordena todos os itens de um formset
    data.djangoInline.setFormOrder();
  });

  // $( "#datepicker" ).datepicker( $.datepicker.regional[ "pt-BR" ] );
  $.fn.datepicker.defaults.format = 'dd/mm/yyyy';
  $.fn.datepicker.defaults.todayBtn = 'linked';
  $.fn.datepicker.defaults.language = 'pt-BR';
  $.fn.datepicker.defaults.autoclose = true;
  $.fn.datepicker.defaults.todayHighlight = true;
  $.fn.datepicker.defaults.enableOnReadonly = true;

  $("#datepicker").datepicker({
    // format: "dd/mm/yyyy",
    // todayBtn: "linked",
    // language: "pt-BR",
    // autoclose: true,
    // todayHighlight: true,
    // enableOnReadonly: false
  });
  // $('.dateinput:not([readonly])').datepicker({
  $('.dateinput').datepicker({
    format: "dd/mm/yyyy",
    todayBtn: "linked",
    language: "pt-BR",
    autoclose: true,
    todayHighlight: true,
    enableOnReadonly: false
  });

  // Remove classe has-error dos FormSetFields
  $('div .has-error').filter('.form-group').has($('div[id^="detail-items-"]')).removeClass('has-error');


  // Os campos que terão máscaras, serão configurados usando 'data-ftl' no html do element
  $("[data-ftl='data']").mask("99/99/9999", {placeholder: "dd/mm/aaaa"});
  $("[data-ftl='datahora']").mask("99/99/9999 99:99", {placeholder: "dd/mm/aaaa hh:mm"});
  $("[data-ftl='telefone']").mask("(99) 9999-999?9");
  $("[data-ftl='celular']").mask("(99) 99999-999?9");
  $("[data-ftl='cpf']").mask("999.999.999-99");
  $("[data-ftl='cnpj']").mask("99.999.999/9999-99");
  $("[data-ftl='cep']").mask("99999-999");

  $('form input:not([type="hidden"]):not([type="submit"])').keydown(function (e) {
    // if (e.keyCode === 13) {
    if (e.key === 'Enter') {
      var inputs = $(this).parents("form").eq(0).find(":input");
      if (inputs[inputs.index(this) + 1] !== null) {
        inputs[inputs.index(this) + 1].focus();
      }
      e.preventDefault();
      return false;
    }
  });

  // $('form div#master-button').insert($('form div:([class="buttons-do-form"])').descendants()[0]);
  $('.tab-content .panel-body').each(function () {
    // $(this).find(".buttons-do-form").appendTo($(this).find("#master-button"));
    // Busca o master-button a partir do pai no tab, que seria o form
    $(this).find(".buttons-do-form").appendTo($(this).parent().find("#master-button"))
  });

  // Configura campos de textarea que serão usados com editor WYSIWYG
  $('.summernote').not("[id*='__prefix__']")
    .summernote({
      toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'underline', 'italic', 'strikethrough', 'superscript', 'subscript', 'clear']],
        ['fontname', ['fontname']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'listStyles', 'paragraph', 'height']],
        ['table', ['table']],
        // ['insert', ['link', 'picture', 'video', 'hr', 'comment']], => de onde é esse comment? Versão antiga
        ['insert', ['link', 'picture', 'video', 'hr']],
        ['specialchars', ['specialchars']],
        ['comment', ['commentDialog', 'commentsShow', 'commentsHide']],
        ['view', ['fullscreen', 'codeview', 'help']],
      ],
      disableDragAndDrop: true,
      disableResizeEditor: true,
      placeholder: 'Conteúdo em HTML',
      tabsize: 2,
      height: 100,
      callbacks: {
        onChange: function (contents, $editable) {
          setHeight($editable);
          // console.log('Summernote onchange');
        },
        onInit: function () {
          // console.log('Summernote is launched');
        },

      },
    });
  // Configura campos de textarea que serão usados com editor WYSIWYG, mas só para leitura e marcação de texto
  $('.summernote-readonly').not("[id*='__prefix__']")
    .summernote({
      toolbar: [
        ['font', ['bold', 'underline', 'italic', 'strikethrough', 'clear']],
        ['color', ['color']],
        ['comment', ['commentDialog', 'commentsShow', 'commentsHide']],
      ],
      disableDragAndDrop: true,
      disableResizeEditor: true,
      placeholder: 'Conteúdo em HTML',
      tabsize: 2,
      height: 100,
      callbacks: {
        onChange: function (contents, $editable) {
          setHeight($editable);
        },
        onPaste: function (e) {
          // var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
          e.preventDefault();
          // document.execCommand('insertText', false, bufferText);
        },
        onKeydown: function (e) {
          e.preventDefault();
        },
        onKeyup: function (e) {
          e.preventDefault();
        },
        onInit: function () {
          // console.log('Summernote-readonly is launched');
        },
      },
    })
    // Desativa drag and drop na área editável (só disableDragAndDrop não funciona)
    .parent().find('.note-editor')
    .on('dragstart', function (e) {
      e.preventDefault();
    })
    .bind('contextmenu', function (e) {
      return false;
    });

  $('.note-toolbar').addClass('fixedElement');
  $('.note-statusbar').hide();
  $('.ext-comment-popover').hide();

  // Força remover o tooltip, está aparecendo erradamente quando edita um conteúdo de documento com o summernote
  $(".tooltip").remove();
  // Autofit altura do summernote
  setHeight($('.note-editable:visible'));
  // Mostra editor pronto
  // $('.summernote, .summernote-readonly').not("[id*='__prefix__']").show();

  // Procura os campos de select com forward e força a atualização da queryset
  // $('select[data-forward-field]').not("[name*='__prefix__']").attr('data-forward-field')
  // JSON.parse($('.dal-forward-conf').not("[id*='__prefix__']").text())
  $('.dal-forward-conf').not("[id*='__prefix__']").each(function () {
    // id destination (conta bancária)
    var id = this.id.replace('dal-forward-conf-for-', '#');
    var dst = $(id);
    var prefix = dst.getFormPrefix();

    var forwardList;
    // Convert forward information into array
    try {
      forwardList = JSON.parse($(this).text());
    } catch (e) {
      return
    }

    forwardList.forEach(function (item) {
      // Bind on source field change (beneficiario)
      $('[name=' + prefix + item.src + ']').on('change', function () {
        // Clear the autocomplete destination
        dst.val(null).trigger('change');
      });
    });
  });

  // Calendário de aluno
  $('.ftl-automount:visible').each(function (index, el) {
    if (
      // check if it has not been mounted yet
      !el._tag
      // // Para montar tags html padrão com data-is, porém não é o caso.
      // && (
      //   // check if it's an unknown html element
      //   el instanceof HTMLUnknownElement ||
      //   // or if it has the data-is attribute
      //   el.getAttribute('data-is')
      // )
    ) {
      riot.mount(el);
      el.classList.remove("ftl-automount");
    }
  });
  // Calendário de aluno
  $('.ftl-calendar:visible').each(function (index, el) {
    update_calendar(el);
  });
}

// rotas de acesso às URLs dos menus
var rotas = [];

function configuraFTL() {
  moment.locale('pt-br');
  //moment.locale();

  configuraPagina();

  // Achando o menu corrente e ativando
  var url = window.location;
  var menu = $('li a[href="' + url.pathname + '"]');
  if (menu.length > 0) {
    menu.parent().addClass('active'); // Ativa a linha que tem o link para a URL atual
    // Ativa o menu que tem a URL contida nele
    $('ul.treeview-menu').filter(function (index) {
      return $("a[href^='" + url.pathname + "']", this).length === 1;
    }).addClass('active').css("display", "block");
  } else {
    if (document.referrer) {
      var a = document.referrer.match(/:\/\/[^\/]+([^\?]*)[\/]*(?:\?.*)?$/)[1];
      if ($('li a[href^="' + a + '"]').length > 0) {
        // Ativa a linha que tem o link para a URL atual
        $('li a[href="' + a + '"]').parent().addClass('active');
        // Ativa o menu que tem a URL contida nele
        $('ul.treeview-menu').filter(function (index) {
          return $("a[href^='" + a + "']", this).length === 1;
        }).addClass('active').css("display", "block");
      }
    }
  }

  // Monta o local das tabs das rotas onde serão mostradas as páginas carregadas
  ftltabs = riot.mount('ftl-tabs')[0];

  // Monta as rotas dos menus
  route('/..', function (name) {
    var url = window.location;
    var current_url = url.hash.slice(1);

    rotas.forEach(function (r, key) {
      if (r.rota === current_url.slice(0, r.rota.length)) {
        var small = '';

        if (url.hash.endsWith('/add/')) small = 'Inclusão';
        else if (url.hash.split("/")[4] === '2') small = 'Alteração';
        else if (url.hash.split("/")[4] === '3') small = 'Exclusão';

//          document.getElementById('h1title').innerHTML = r.nome + '<small>'+small+'</small>';

        ftltabs.trigger('updateRoute', key, r.nome, current_url, small, r.reload);
      }
    });
  });

  route.start(true);
}

// Controle elementos fixos para scroll, exemplo: toolbar do summernote na edição de conteúdo quando rola a tela
$(window).scroll(function (e) {
  var $el = $('.fixedElement:visible');
  var isPositionFixed = ($el.css('position') === 'fixed');
  if ($(this).scrollTop() > 260 && !isPositionFixed) {
    $el.css({'position': 'fixed', 'top': '0px'});
  }
  if ($(this).scrollTop() <= 260 && isPositionFixed) {
    $el.css({'position': 'static', 'top': '0px'});
  }
  // console.log('parent width', $el.parent().width());
  $el.css({'width': $el.parent().find('.note-editing-area').width() + 'px'});
});

function formset_up(e) {
  var $e = $(e);
  var $djinline = $e.closest('.js-django-inlines').data().djangoInline;
  var index = $djinline.getFormIndex(e);
  $djinline.moveFieldUp(index);
}

function formset_down(e) {
  var $e = $(e);
  var $djinline = $e.closest('.js-django-inlines').data().djangoInline;
  var index = $djinline.getFormIndex(e);
  $djinline.moveFieldDown(index);
}

function update_calendar(elem) {
  var url = elem.dataset.url;
  $.ajax({
    type: 'GET',
    url: url,
    // data: dados,
    success: function (data) {
      var calendar = new FullCalendar.Calendar(elem, {
        plugins: ['dayGrid'],
        // defaultView: 'dayGridWeek',
        header: {
          center: 'dayGridMonth,dayGridWeek' // buttons for switching between views
        },
        eventRender: function (info) {
          info.el.setAttribute('data-container', 'body');
          info.el.setAttribute('data-toggle', 'tooltip');
          info.el.setAttribute('data-html', 'true');
          info.el.setAttribute('data-placement', 'auto');
          info.el.setAttribute('title', info.event.extendedProps.description);
        },
        timeZone: "local",
        locale: 'pt-BR',
        draggable: false,
        droppable: false,
        height: $(window).height() * 0.8,
        contentHeight: 'auto',
        events: data,
        loading: function (bool) {
          if (bool) $('#loading').show();
          else $('#loading').hide();
        },
      });
      calendar.render();
    },
    error: function (data) {
      console.log('Erro no ajax do calendar');
    }
  });
}

// // Monitora DOM e monta automaticamente riotjs tag ainda não montada (_tag não existe) e class ftl-automount
// var appFTL = document.querySelector('body');
// // all the nodes appended into the body will pass from here
// appFTL.addEventListener('DOMNodeInserted', function (e) {
//   var node = e.target;
//   // check if it's a tag node
//   if (node.nodeType === 1) { // 1 = element, 2 = attribute, 3 = text, 4 = comment
//     node.querySelectorAll('.ftl-automount').forEach(function (el) {
//       if (
//         // check if it has not been mounted yet
//         !el._tag
//         // // Para montar tags html padrão com data-is, porém não é o caso.
//         // && (
//         //   // check if it's an unknown html element
//         //   el instanceof HTMLUnknownElement ||
//         //   // or if it has the data-is attribute
//         //   el.getAttribute('data-is')
//         // )
//       ) {
//         // riot.mount(el);
//         // el.classList.remove("ftl-automount");
//       }
//
//     });
//   }
// }, false);
