<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="AJAX Request Movie" :desc="desc">
        <button class="btn btn-secondary sweet-15" type="button" @click="movieAlert()">Movie mode</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Give the movie name & return value.")
function movieAlert() {
    Swal.fire({
        text: 'Search for a movie. e.g. "Herry Poter".',
        input: "text",
    })
        .then((name) => {
            if (!name) throw null;

            return fetch(
                `https://itunes.apple.com/search?term=${name.value}&entity=movie`
            );
        })
        .then((results) => {
            return results.json();
        })
        .then((json) => {
            const movie = json.results[0];

            if (!movie) {
                return Swal.fire("No movie was found!");
            }
            const name = movie.trackName;
            const imageURL = movie.artworkUrl100;
            Swal.fire({
                imageUrl: imageURL,
                text: name,
            });
        })
        .catch((err) => {
            if (err) {
                Swal.fire("Oh noes!", "The AJAX request failed!", "error");
            }
        });
}
</script>