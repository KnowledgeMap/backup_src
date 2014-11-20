/**
 * @author whenlove
 */


/* 测试文本
1001(a,b)
10000011(b,c,d)
10000011(d,e,f)
10000011(f,g,h)
10000011(h,i,j)
10000011(j,k,l)
*/

var raphael_top;
var raphael_canvas;
//var all_raphael_set;
var boole_rect = new Object();
var boole_text = new Object();
//var rect_type = new Object();

// 验证节点是否变化
var boole_data = new Object();

// 传参用
var rule_data;

var target_text,
    target_id = '',
    store_id = '';

var canvas_width = 800,
    canvas_height = 500,
    canvas_x = 420,
    canvas_y = 50,
    rect_width = 30,
    rect_height = 30,
    rect_x = rect_width/2,
    rect_y = rect_height/2,
    img_width = 30,
    img_height = 30,
    img_x = img_width/2,
    img_y = img_height/2;

jQuery(document).ready(function(){
    //$('#rule_text').val('1001(韩梅梅,b)\n10000011(b,c,d)\n10000011(d,e,f)\n10000011(f,g,h)\n10000011(h,i,j)\n10000011(j,k,l)');
    $('#rule_text').val('11101001(a=b,a=c,b=c)\n11101001(a=b,a=e,b=e)\n11101001(b=e,c=e,b=c)\n11101001(a=e,a=c,c=e)');
    // jQuery.ajax({
        // type: "GET",
        // url: "svg/11101111.svg",
        // dataType: "text",
        // success: function(svgXML) {
          // svg_1001 = svgXML;
        // }
    // });
});

function startDraw(graph){
    clearCanvas();
    
    var color = d3.scale.category20();
    
    var force = d3.layout.force().charge(-200).linkDistance(100).alpha(.0001).size([canvas_width, canvas_height]);
    
    var svg = d3.select("body").append("svg").attr("width", canvas_width).attr("height", canvas_height);
    
    //d3.json("boole.json", function(error, graph) {
    //d3.json("test.json", function(error, graph) {
    //console.info(graph.nodes);
    //console.info(graph.links);
    
        force.nodes(graph.nodes).links(graph.links).start();
        
        while (force.alpha() > 0.005)
            force.tick();
        force.stop();
        
        // 开始绘制
        //raphael_canvas.setStart();
        
        for (var the_node in graph.links) {
            raphael_canvas.path("M" + graph.links[the_node]['source']['x'] +  "," + graph.links[the_node]['source']['y'] + "L" + graph.links[the_node]['target']['x'] +  "," + graph.links[the_node]['target']['y'])
            .attr({stroke: '#0000ff', "stroke-width": 1, "stroke-opacity": 0.5})
        }
        
        
        for (var the_node in graph.nodes) {
            var the_node_name = graph.nodes[the_node]['name'];
            //console.info(the_node_name);
            
            // --------- 0
            if(graph.nodes[the_node]['group'] == '0'){
                boole_rect[the_node_name] = raphael_canvas
                .rect(graph.nodes[the_node]['x'] - rect_x, graph.nodes[the_node]['y'] - rect_y, rect_width, rect_height, 6)
                .attr({
                    fill : "#ffffff",
                    stroke : "#1C262F",
                    "fill-opacity" : 1,
                    "stroke-width" : 2
                })
                
                boole_rect[the_node_name]['type'] = 'other';
                boole_rect[the_node_name]['name'] = the_node_name;
                boole_data[the_node_name] = '0';
                
                boole_rect[the_node_name].click(function () {
                    console.info(this['name'], this['type']);
                    // 初始时，无关节点
                    if(this['type'] == 'other'){
                        if(boole_data[this['name']] == '0'){
                            this.animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            this.animate({fill : "#ffffff"}, 300);
                            boole_data[this['name']] = '0';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // 目标节点
                    if(this['type'] == 'target'){
                        boole_data[this['name']] = '1';
                        target_id = this['name'];
                        target_text.attr({'text':'target :  ' + this['name']});
                    }
                    
                    // 下游节点
                    if(this['type'] == 'next'){
                        if(target_id != this['name']){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            node_color = boole_rect[this['name']]['next_color'];
                            //boole_rect[this['name']].animate({fill : "#228844"}, 300);
                            boole_rect[this['name']].animate({fill : node_color}, 300);
                            boole_data[this['name']] = '1';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // path节点
                    if(this['type'] == 'path'){
                        if(target_id != this['name']){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            boole_rect[this['name']].animate({fill : "#ff6600"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // zero节点
                    if(this['type'] == 'zero'){
                        if(target_id != this['name']){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            boole_rect[this['name']].animate({fill : "#ff3838"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // store节点
                    if(this['type'] == 'store'){
                        //alert('你真的掌握这个知识点了吗？');
                        console.info('=====================',target_id);
                        if(target_id = store_id){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        
                        else {
                            if(target_id != this['name']){
                                
                                boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                                boole_data[this['name']] = '1';
                                target_id = this['name'];
                                target_text.attr({'text':'target  :  ' + this['name']});
                            }
                            
                            else{
                                boole_rect[this['name']].animate({fill : "#3388ff"}, 300);
                                boole_data[this['name']] = '1';
                                target_id = '';
                                target_text.attr({'text':'target  :  '});
                            }
                        }
                    }
                });

                boole_text[the_node_name] = raphael_canvas.text(graph.nodes[the_node]['x'], graph.nodes[the_node]['y'], the_node_name)
                .attr({fill: "#000", "font-size":10, "text-anchor":"middle", "font-weight": "bold"});
                
                boole_text[the_node_name]['name'] = the_node_name;
                boole_text[the_node_name]['type'] = 'other';
                boole_text[the_node_name].click(function () {
                    console.info(this['name'], this['type']);
                    // 初始时，无关节点
                    if(this['type'] == 'other'){
                        if(boole_data[this['name']] == '0'){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            boole_rect[this['name']].animate({fill : "#ffffff"}, 300);
                            boole_data[this['name']] = '0';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // 目标节点
                    if(this['type'] == 'target'){
                        boole_data[this['name']] = '1';
                        target_id = this['name'];
                        target_text.attr({'text':'target :  ' + this['name']});
                    }
                    
                    // 下游节点
                    if(this['type'] == 'next'){
                        if(target_id != this['name']){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            node_color = boole_rect[this['name']]['next_color'];
                            //boole_rect[this['name']].animate({fill : "#228844"}, 300);
                            boole_rect[this['name']].animate({fill : node_color}, 300);
                            boole_data[this['name']] = '1';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // path节点
                    if(this['type'] == 'path'){
                        if(target_id != this['name']){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            boole_rect[this['name']].animate({fill : "#ff6600"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // zero节点
                    if(this['type'] == 'zero'){
                        if(target_id != this['name']){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        else{
                            boole_rect[this['name']].animate({fill : "#ff3838"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = '';
                            target_text.attr({'text':'target  :  '});
                        }
                    }
                    
                    // store节点
                    if(this['type'] == 'store'){
                        //alert('你真的掌握这个知识点了吗？');
                        console.info('=====================',target_id);
                        if(target_id = store_id){
                            boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                            boole_data[this['name']] = '1';
                            target_id = this['name'];
                            target_text.attr({'text':'target  :  ' + this['name']});
                        }
                        
                        else {
                            if(target_id != this['name']){
                                
                                boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                                boole_data[this['name']] = '1';
                                target_id = this['name'];
                                target_text.attr({'text':'target  :  ' + this['name']});
                            }
                            
                            else{
                                boole_rect[this['name']].animate({fill : "#3388ff"}, 300);
                                boole_data[this['name']] = '1';
                                target_id = '';
                                target_text.attr({'text':'target  :  '});
                            }
                        }
                    }
                });
            
            }
            
            // --------- 1
            /*
            if(graph.nodes[the_node]['group'] == '1'){

                
                boole_rect[the_node_name] = raphael_canvas
                .rect(graph.nodes[the_node]['x'] - rect_x, graph.nodes[the_node]['y'] - rect_y, rect_width, rect_height, 6)
                .attr({
                    fill : "#3390F7",
                    stroke : "#1C262F",
                    "fill-opacity" : 1,
                    "stroke-width" : 2
                })
                
                boole_rect[the_node_name]['name'] = the_node_name;
                boole_data[the_node_name] = '1';
                
                boole_rect[the_node_name].click(function () {
                    //console.info(this['name']);
                    //console.info(boole_data[this['name']]);
                    if(boole_data[this['name']] == '0'){
                        this.animate({fill : "#dd00ff"}, 300);
                        boole_data[this['name']] = '1';
                        target_id = this['name'];
                        target_text.attr({'text':'target:  ' + this['name']});
                    }
                    else{
                        this.animate({fill : "#ffffff"}, 300);
                        boole_data[this['name']] = '0';
                        target_id = '';
                        target_text.attr({'text':'target  :  '});
                    }
                });

                boole_text[the_node_name] = raphael_canvas.text(graph.nodes[the_node]['x'], graph.nodes[the_node]['y'], the_node_name)
                .attr({fill: "#000", "font-size":10, "text-anchor":"middle", "font-weight": "bold"});
                
                boole_text[the_node_name]['name'] = the_node_name;
                
                boole_text[the_node_name].click(function () {
                    if(boole_data[this['name']] == '0'){
                        boole_rect[this['name']].animate({fill : "#dd00ff"}, 300);
                        boole_data[this['name']] = '1';
                        target_id = this['name'];
                        target_text.attr({'text':'target:  ' + this['name']});
                    }
                    else{
                        boole_rect[this['name']].animate({fill : "#ffffff"}, 300);
                        boole_data[this['name']] = '0';
                        target_id = '';
                        target_text.attr({'text':'target  :  '});
                    }
                });
                
            }
            */
            
            if(graph.nodes[the_node]['group'] == '2'){
                raphael_canvas.image("image/11.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '3'){
                raphael_canvas.image("image/1001.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '4'){
                raphael_canvas.image("image/1011.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '5'){
                raphael_canvas.image("image/10000011.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '6'){
                raphael_canvas.image("image/11000001.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '7'){
                raphael_canvas.image("image/11100001.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '8'){
                raphael_canvas.image("image/10001011.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '9'){
                raphael_canvas.image("image/11101001.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '10'){
                raphael_canvas.image("image/11001011.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '11'){
                raphael_canvas.image("image/10001111.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '12'){
                raphael_canvas.image("image/11101011.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
            
            if(graph.nodes[the_node]['group'] == '13'){
                raphael_canvas.image("image/11101111.png",graph.nodes[the_node]['x'] - img_x, graph.nodes[the_node]['y'] - img_y, img_width, img_height);
            }
        }
        
        //all_raphael_set = raphael_canvas.setFinish();
    //});
}

function startInductionChange(graph){
    //console.info(graph.info);
    //console.info(graph.info['path']);
    //console.info(graph.info['zero']);
    //console.info(graph.info['target']);
    //console.info(graph.info['store']);
    
    path_array = graph.info['path'];
    zero_array = graph.info['zero'];
    target_array = graph.info['target'];
    store_array = graph.info['store'];
    
    var oo = new Object();
    
    
    for (var the_path in path_array) {
        var the_node_name = graph.nodes[path_array[the_path]]['name'];
        console.info('the_path', path_array[the_path], the_node_name);
        boole_rect[the_node_name].animate({fill : "#ff6600"}, 100);
        boole_data[the_node_name] = '1';
        boole_rect[the_node_name]['type'] = 'path';
        boole_text[the_node_name]['type'] = 'path';
        oo[the_node_name] = '1';
    }
    
    for (var the_zero in zero_array) {
        var the_node_name = graph.nodes[zero_array[the_zero]]['name'];
        console.info('the_zero', zero_array[the_zero], the_node_name);
        boole_rect[the_node_name].animate({fill : "#ff3838"}, 100);
        boole_data[the_node_name] = '1';
        boole_rect[the_node_name]['type'] = 'zero';
        boole_text[the_node_name]['type'] = 'zero';
        oo[the_node_name] = '1';
    }
    
    for (var the_target in target_array) {
        var the_node_name = graph.nodes[target_array[the_target]]['name'];
        console.info('the_target', target_array[the_target], the_node_name);
        boole_rect[the_node_name].animate({fill : "#dd00ff"}, 100);
        boole_data[the_node_name] = '1';
        boole_rect[the_node_name]['type'] = 'target';
        boole_text[the_node_name]['type'] = 'target';
        oo[the_node_name] = '1';
    }
    
    for (var the_store in store_array) {
        var the_node_name = graph.nodes[store_array[the_store]]['name'];
        console.info('the_store', store_array[the_store], the_node_name);
        boole_rect[the_node_name].animate({fill : "#3388ff"}, 100);
        boole_data[the_node_name] = '1';
        boole_rect[the_node_name]['type'] = 'store';
        boole_text[the_node_name]['type'] = 'store';
        oo[the_node_name] = '1';
        store_id = the_node_name;
    }
    for (var the_node in graph.nodes) {
        if(graph.nodes[the_node]['group'] == '0' || graph.nodes[the_node]['group'] == '1'){
            var the_node_name = graph.nodes[the_node]['name'];
            if (oo[the_node_name]){
                //console.info('+++',the_node_name);
            }
            else{
                //console.info('---',the_node_name);
                boole_rect[the_node_name].animate({fill : "#ffffff"}, 100);
                boole_data[the_node_name] = '0';
                boole_rect[the_node_name]['type'] = 'other';
                boole_text[the_node_name]['type'] = 'other';
            }
        }
    }
}

function startDeductionChange(graph){
    
    for (var the_node in graph.nodes) {
        var the_node_name = graph.nodes[the_node]['name'];
        if(graph.nodes[the_node]['group'] == '0' || graph.nodes[the_node]['group'] == '1'){
            var the_fuzzy = graph.nodes[the_node]['fuzzy'];
            //var scale = chroma.scale(["#ffffff", "#22B14C" ]);
            //console.info(typeof(the_fuzzy));
            if(the_fuzzy == 1.0){
                // 目标节点
                if (the_node_name == target_id){
                    boole_rect[the_node_name].animate({fill : "#dd00ff"}, 100);
                    boole_data[the_node_name] = '1';
                    boole_rect[the_node_name]['type'] = 'target';
                    boole_text[the_node_name]['type'] = 'target';
                }
                // 其它1是下游节点
                else{
                    boole_rect[the_node_name].animate({fill : "#228844"}, 100);
                    boole_data[the_node_name] = '1';
                    boole_rect[the_node_name]['type'] = 'next';
                    boole_text[the_node_name]['type'] = 'next';
                    boole_rect[the_node_name]['next_color'] = "#228844";
                }
            }
            else{
                // 无关节点
                if(the_fuzzy == 0.0){
                    boole_rect[the_node_name].animate({fill : "#ffffff"}, 100);
                    boole_data[the_node_name] = '0';
                    boole_rect[the_node_name]['type'] = 'other';
                    boole_text[the_node_name]['type'] = 'other';
                }
                // 其它下游节点
                else{
                    //node_color = scale(the_fuzzy);
                    var c1 = 255-221*the_fuzzy,
                        c2 = 255-119*the_fuzzy,
                        c3 = 255-187*the_fuzzy;
                    
                    node_color = 'rgb(' + c1.toString() +',' + c2.toString() + ',' + c3.toString() + ')';
                    console.info(the_fuzzy);
                    console.info(node_color);
                    boole_rect[the_node_name].animate({fill : node_color}, 100);
                    boole_data[the_node_name] = '1';
                    
                    boole_rect[the_node_name]['type'] = 'next';
                    boole_text[the_node_name]['type'] = 'next';
                    boole_rect[the_node_name]['next_color'] = node_color;
                }
            }
        

       } 
    }
}

function clearCanvas(){
    //all_raphael_set.clear();
    boole_rect = new Object();
    boole_text = new Object();
    boole_data = new Object();
    raphael_canvas.clear();
}

function resetRect(){
    //console.info(boole_data);
    for(var s in boole_data){
        
        //if(boole_data[s] == '1'){
        boole_data[s] = '0';
        boole_rect[s].animate({fill : "#ffffff"}, 100);
        boole_rect[s]['type'] = 'other';
        boole_text[s]['type'] = 'other';
        boole_rect[s]['next_color'] = "#ffffff";
        target_id = '';
        target_text.attr({'text':'target  :  '});
        //}
    }
}

function startDeduction(){
    if (target_id != ''){
        var node_str = '';
        for(var s in boole_data){
            node_str = node_str + s + '====' + boole_data[s] + '----';
        }
        $.post('/start_change/',{'data':rule_data, 'node_str':node_str, 'flag': 'deduction', 'target_name': target_id},function(ajax){
            if(ajax.res == "right"){
                startDeductionChange(ajax.data);
            }
            else{
                $('#rule_text').val(rule_data + '\n' + ajax.data);
            }
        },"json")
    }
    else{
        resetRect();
    }
}

function startInduction(){
    if (target_id != ''){
        if(target_id != store_id){
        
            var node_str = '';
            for(var s in boole_data){
                node_str = node_str + s + '====' + boole_data[s] + '----';
            }
            $.post('/start_change/',{'data':rule_data, 'node_str':node_str, 'flag': 'induction', 'target_name': target_id, 'store_name': store_id},function(ajax){
                if(ajax.res == "right"){
                    startInductionChange(ajax.data);
                }
                else{
                    //$('#rule_text').val('报错了');
                    $('#rule_text').val(rule_data + '\n' + ajax.data);
                }
            },"json")
        }
        else{
            alert('你真的掌握这个知识点了吗？');
            boole_rect[target_id].animate({fill : "#3388ff"}, 300);
            boole_data[target_id] = '1';
            target_id = '';
            target_text.attr({'text':'target  :  '});
        }
    }
    else{
        alert('执行Induction前，请先选择一个target节点');
    }
}

function deleteRule(){
    //$('#rule_text').val() = '';
    $('#rule_text').val("");
}


function loadRule(){
    resetRect();
    //console.info($('#rule_text').val());
    var data = $('#rule_text').val();
    rule_data = $('#rule_text').val();
    //console.info(data);
    /*
    var funcs = [];
    
    var lines = data.split('\n');
    for (i = 0; i < lines.length; i++) {
        //console.info(lines[i]);
        func_obj = new Object();
        var func = lines[i].split('(')[0];
        var params = lines[i].split('(')[1].replace(')','');
        params = params.split(',')
        
        func_obj['params'] = params;
        func_obj[func] = func;
        
        funcs.push(func_obj);
        
        // 太2了，用python拆分不就完了吗！
        console.info(func_obj);
        //console.info(func);
        for (p = 0; p < params.length; p++) {
            //console.info(params[p]);
        }
    }
    console.info(funcs);
    */
    // 传给 解析后端模块
    
    //console.info('11111111111');
    $.post('/start_layout/',{'data':data},function(ajax){
        //console.info('222222222');
        if(ajax.res == "right"){
            //$('#rule_text').val(ajax.data);
            //console.info(ajax.data.nodes);
            startDraw(ajax.data);
        }
        else{
            //$('#rule_text').val('报错了');
            $('#rule_text').val(rule_data + '\n' + ajax.data);
        }
    },"json")
    
    
    // 从解析模块获取返回值，先用json代替
    //the_json = 'aaa';
    //startDraw(the_json);
    
}

Raphael(0, 0, 1680, 800, function () {
    // 定义整体空间
    raphael_top = this;
    raphael_top.rect(canvas_x, canvas_y, canvas_width, canvas_height, 0).attr({
        fill:"#ffffff",
        "fill-opacity": 1,
        stroke:"#0000ff",
        "stroke-opacity": 1,
        
    });
    
    // target
    raphael_top.rect(canvas_x + 2, canvas_y + 2, 160, 30, 0).attr({
        fill:"#C9E3F5",
        "fill-opacity": 0.7,
        stroke:"#0000ff",
        "stroke-opacity": 0,
        
    });
    target_text = raphael_top.text(canvas_x + 2 + 15, canvas_y + 2 + 15, 'target  : ').attr(
        {fill: "#000", "font-size":16, "opacity": 1, "text-anchor":"start"}
    )
    
    raphael_top.rect(50, 580, 120, 40, 0).attr({
        fill:"#444546",
        "fill-opacity": 0.7,
        "stroke-opacity": 0,
        
    }).click(
        loadRule
    );
    
    raphael_top.text(110, 600, '确 定').attr(
        {fill: "#000", "font-family":"微软雅黑", "font-size":18, "opacity": 1, "text-anchor":"middle", "font-weight": "bold"}
    ).click(
        loadRule
    );
    
    
    raphael_top.rect(240, 580, 120, 40, 0).attr({
        fill:"#444546",
        "fill-opacity": 0.7,
        "stroke-opacity": 0,
        
    }).click(
        deleteRule
    );
    
    raphael_top.text(300, 600, '清 空').attr(
        {fill: "#000", "font-family":"微软雅黑", "font-size":18, "opacity": 1, "text-anchor":"middle", "font-weight": "bold"}
    ).click(
        deleteRule
    );
    
    raphael_top.rect(540, 580, 150, 40, 0).attr({
        fill:"#444546",
        "fill-opacity": 0.7,
        "stroke-opacity": 0,
        
    }).click(
        startDeduction
    );
    
    raphael_top.text(615, 600, 'Deduction').attr(
        {fill: "#000", "font-family":"微软雅黑", "font-size":18, "opacity": 1, "text-anchor":"middle", "font-weight": "bold"}
    ).click(
        startDeduction
    );
    
    raphael_top.rect(790, 580, 150, 40, 0).attr({
        fill:"#444546",
        "fill-opacity": 0.7,
        "stroke-opacity": 0,
        
    }).click(
        startInduction
    );
    
    raphael_top.text(865, 600, 'Induction').attr(
        {fill: "#000", "font-family":"微软雅黑", "font-size":18, "opacity": 1, "text-anchor":"middle", "font-weight": "bold"}
    ).click(
        startInduction
    );
    
    raphael_top.rect(1040, 580, 150, 40, 0).attr({
        fill:"#444546",
        "fill-opacity": 0.7,
        "stroke-opacity": 0,
        
    }).click(
        resetRect
    );
    
    raphael_top.text(1115, 600, '重置').attr(
        {fill: "#000", "font-family":"微软雅黑", "font-size":18, "opacity": 1, "text-anchor":"middle", "font-weight": "bold"}
    ).click(
        resetRect
    );
    
    
    //console.info('aaa');
})

Raphael(canvas_x, canvas_y, canvas_width, canvas_height, function () {
    // 定义整体空间
    raphael_canvas = this;
    raphael_canvas.rect(0, 0, canvas_width, canvas_height, 0).attr({
        fill:"#ffffff",
        "fill-opacity": 1,
        "stroke-opacity": 0,
        
    });
    
    
})