// const api_host='http://127.0.0.1:5000'

var vm = new Vue({
    el: '#app',
    data: {
        debug: false,

        tokenizer_list: {},
        dict_based_tokenizer: {},

        server: "https://api.xiaoquankong.ai/tokenizer",
        message: "王小明在北京的清华大学读书。",
        custom_dict_message: "王小明在上海的饿了么实习。",
        fusion_message: "王小明在网易杭州的杭研大厦工作。",

        use_custom_dict: false,
        custom_dict: "饿了么\n杭研大厦 12",

        tokenizer_class: '',
        dict_based_tokenizer_class: '',
        fusion_tokenizer_class: [],

        token_list: {},
        dict_based_token_list: {},
        fusion_based_token_list: {}
    },
    created: function () {},
    methods: {
        send_tokenize_request: function () {
            vm.axios.get(vm.server + '/single_tokenizer', {
                'message': vm.message,
                'tokenizer_class': vm.tokenizer_class
            })
                .then(function (response) {
                    console.log(response.data);
                    vm.token_list = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                })
                .then(function () {
                    // always executed
                });
        }
    }
})

// Optionally the request above could also be done as

vm.axios.get(vm.server + '/list_tokenizer')
    .then(function (response) {
        console.log(response.data);
        vm.tokenizer_list = response.data;
    })
    .catch(function (error) {
        console.log(error);
    })
    .then(function () {
        // always executed
    });

vm.axios.get(vm.server + '/list_dict_based_tokenizer')
    .then(function (response) {
        console.log(response.data);
        vm.dict_based_tokenizer = response.data;
    })
    .catch(function (error) {
        console.log(error);
    })
    .then(function () {
        // always executed
    });

var send_tokenize_request = function () {
    vm.axios.get(vm.server + '/single_tokenizer', {
        params: {
            'message': vm.message,
            'tokenizer_class': vm.tokenizer_class
        }
    })
        .then(function (response) {
            console.log(response.data);
            vm.token_list = response.data;
        })
        .catch(function (error) {
            console.log(error);
        })
        .then(function () {
            // always executed
        });
}

var send_tokenize_request_with_custom_dict = function () {
    vm.axios.get(vm.server + '/single_tokenizer_with_custom_dict', {
        params: {
            'message': vm.custom_dict_message,
            'tokenizer_class': vm.dict_based_tokenizer_class,
            'custom_dict': vm.use_custom_dict ? vm.custom_dict : ''
        }
    })
        .then(function (response) {
            console.log(response.data);
            vm.dict_based_token_list = response.data;
        })
        .catch(function (error) {
            console.log(error);
        })
        .then(function () {
            // always executed
        });
}

var send_tokenize_request_with_fusion = function () {
    vm.axios.get(vm.server + '/tokenizer_with_fusion', {
        params: {
            'message': vm.fusion_message,
            'tokenizer_class_list': vm.fusion_tokenizer_class,
        }
    })
        .then(function (response) {
            console.log(response.data);
            vm.fusion_based_token_list = response.data;
        })
        .catch(function (error) {
            console.log(error);
        })
        .then(function () {
            // always executed
        });
}
