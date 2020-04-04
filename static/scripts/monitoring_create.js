//faz a busca de pacientes pelo nome, cpf, rg... durante a criação de atendimetos
        var div_profiles = $("#profiles");//aqui onde ele vai mostrar os pacientes encontrados
        var button = $("#search_profile_button");//aqui o botão onde clicka pra buscar
        var search_input = $("#search-profile");//aqui o valor informado pra busca

        button.on('click', () => {
            var term = search_input.val();
            $.get("/pacientes/" + term +"/buscar", (profiles, status) => {

                div_profiles.html("");

                if (profiles.length == 0) {//não achou pacientes
                    //Aqui é uns html pra deixar no padrão do crispy form...
                    var div = $("<div class='form-check'></div>");
                    var input = $('<input type="radio" class="form-check-input" name="profile" id="id_profile_1" hidden value="">');

                    var span = $('<label for="id_profile_1" class="form-check-label"></label')
                            .text("Não foram encontrados pacientes.");

                    div.append(input);
                    div.append(span);

                    div_profiles.append(div);
                    //div_profiles.html("Não foi encontrado pacientes.")
                }
                else {
                    profiles.forEach( (profile) => {//achou pacientes
                        //Aqui é uns html pra deixar no padrão do crispy form...
                        var div = $("<div class='form-check'></div>");
                        var input = $('<input type="radio" class="form-check-input" name="profile" id="id_profile_' +profile.id +' ">');

                        var span = $('<label for="id_profile_' +profile.id +' " class="form-check-label"></label')
                            .text(profile.full_name + ", cpf: "+profile.cpf);

                        input.val(profile.id);
                        div.append(input);
                        div.append(span);

                        div_profiles.append(div);
                    });
                }
            })
        });