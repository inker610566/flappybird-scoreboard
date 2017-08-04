<template>
    <div class="hello">
        <h1 @click="debug = !debug">Flappy Bird Ranking</h1>
        <div v-show="debug">
            <input v-model="fake_name">
            <input v-model="fake_score">
            <button @click="submit_score">submit</button>
        </div>
        <ul>
            <transition-group name="list">
            <li v-for="r, i in rank" :key="r" :class="{first: i==0, second: i==1, third: i==2, others: i>2}">
                <div class="field rank-no">{{ i+1 }}</div><div class="field name">{{ r.name }}</div><div class="field score">{{ r.score }}</div>
            </li>
            </transition-group>
        </ul>
    </div>
</template>

<script>
import $ from 'jquery';

export default {
    name: 'hello',
    data () {
        return {
            rank: [
            ],
            debug: false,
            fake_name: '',
            fake_score: '0',
        };
    },
    mounted() {
        this.refresh_loop();
    },
    methods: {
        async sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
        async refresh_loop() {
            while(true) {
                await this.refresh_socreboard();
                await this.sleep(1000);
            }
        },
        async refresh_socreboard() {
            try {
                let response = await fetch(new Request('http://localhost:8000/score', {
                    method: 'GET'
                }));
                let json = await response.json()
                let new_rank = json.data.sort((a, b)=> b.score-a.score);
                let i = 0;
                for(; i < this.rank.length ; i ++)
                {
                    this.rank.splice(i, 1);
                    if(i < new_rank.length)
                        this.rank.splice(i, 0, new_rank[i]);
                    await this.sleep(1000);
                }
                while(i < new_rank.length) {
                    this.rank.push(new_rank[i]);
                    i ++;
                    await this.sleep(1000);
                }
            } catch(e) {
                console.log(e);
            }
        },
        submit_score() {
            let score = parseInt(this.fake_score);
            $.post('http://localhost:8000/score', {
                name: this.fake_name,
                score
            }, (data) => {
                console.log(data);
            });
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
    font-weight: normal;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    padding: 18px 10px 18px 50px;
}

.list-item {
  display: inline-block;
  margin-right: 10px;
}

.list-enter-active, .list-leave-active {
    transition: all 1s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
    transform: translateX(10px);
    opacity: 0;
}

.field {
    display: inline-block;
    padding: 10px 10px;
}

.name {
    width: 10em;
    text-align: left;
}

.first {
    background: gold;
    color: GoldenRod;
    font-weight: bold;
}

.second {
    background: silver;
    color: white;
    font-weight: bold;
}

.third {
    /*background: coral;*/
    background: #EE7F50;
    color: gold;
    font-weight: bold;
}

.rank-no {
}
</style>
