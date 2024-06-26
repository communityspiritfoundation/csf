<template>
  <div v-if="!loading">
    <v-container>
      <v-row class="ma-0 px-13" align="center" justify="center">
        <v-col align="center">
          <h1>Welcome back, {{ userStore.user!.username }}</h1>
        </v-col>
        <v-btn size="medium" icon="mdi-cog" variant="text" href="/settings" />
      </v-row>
      <v-divider />
      <v-row class="ma-0 px-4 pb-0 pt-0" align="center">
        <v-col>
          <v-card variant="flat" class="pb-1">
            <v-container class="pa-0" fluid>
              <v-row class="ma-0">
                <v-row align="center" class="my-1">
                  <v-icon :class="['mdi', 'ml-2', method]" size="52" color="#2c3d4f" />
                  <v-col class="pb-0">
                    <v-chip color="green" class="rounded text-h5"
                      >{{ Math.round(mileageStore.totalKmByUser * 100) / 100 }} KM</v-chip
                    >
                    <h3>TOTAL</h3>
                  </v-col>
                </v-row>

                <v-spacer />
                <v-col cols="auto">
                  <v-btn
                    variant="elevated"
                    elevated="2"
                    :ripple="true"
                    icon="mdi-plus"
                    color="primaryRed"
                    @click="dialog = true"
                  />
                  <MileageModal v-model="dialog" @handle-submit="updateChallengeProgress(true)" />
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
      <v-divider />
      <v-row class="ma-0 pt-0 pb-0" align="center">
        <v-col>
          <h2>Daily KMs</h2>
          <MileageGraph :dataPoints="mileageStore.mileageByUser" />
        </v-col>
      </v-row>

      <div class="px-2">
        <h2>Challenges</h2>
        <div v-for="challenge in challenges" :key="challenge.name" class="my-4">
          <h3>{{ challenge.name }}</h3>
          <v-row dense>
            <v-col>
              <div class="progress-bar rounded-lg">
                <div
                  :class="`rounded-lg ${challenge.colour}`"
                  :style="`width: ${calcWidth(
                    mileageStore.totalChallengeKmByUser,
                    challenge.length
                  )}%`"
                ></div>
              </div>
            </v-col>
            <v-col cols="4" sm="2" lg="1">
              <div :class="`length-label rounded-lg ${challenge.colour}`">
                <h3 class="primaryWhite text-center">
                  {{ `${mileageStore.totalChallengeKmByUser}/${challenge.length}KM` }}
                </h3>
              </div>
            </v-col>
          </v-row>
        </div>
      </div>
      <v-divider />
    </v-container>
  </div>

  <ChallengeCompletePopupModalVue
    v-model="isCompleted"
    :challenge-name="challengeName"
  ></ChallengeCompletePopupModalVue>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MileageModal from '../components/MileageModal.vue'
import { useUserStore } from '@/stores/user'
import { useMileageStore } from '@/stores/mileage'
import ChallengeCompletePopupModalVue from '@/components/ChallengeCompletePopupModal.vue'
import MileageGraph from '../components/MileageGraph.vue'

const userStore = useUserStore()
const mileageStore = useMileageStore()

const method = ref()
const loading = ref(true)
const isCompleted = ref(false)
const challengeName = ref('')

const getIconName = (medium: any) => {
  switch (medium) {
    case 'RUNNING':
      method.value = 'mdi-run-fast'
      break
    case 'WHEELING':
      method.value = 'mdi-wheelchair-accessibility'
      break
    case 'WALKING':
      method.value = 'mdi-walk'
      break
  }
}

const dialog = ref(false)
const challenges = ref([
  { name: 'WOORABINDA', length: 24, colour: 'bg-secondaryGreen' },
  { name: 'WURRUMIYANGA', length: 60, colour: 'bg-secondaryBlue' },
  { name: "GALIWIN'KU", length: 84, colour: 'bg-primaryRed' },
  { name: 'PALM ISLAND', length: 120, colour: 'bg-primaryBlack' }
])

function calcWidth(travelDist: number, totalDist: number) {
  return Math.min((100 * travelDist) / totalDist, 100)
}

async function updateChallengeProgress(checkForCompletion: boolean) {
  const oldDistance = mileageStore.totalChallengeKmByUser
  await mileageStore.getChallengeMileage()

  if (checkForCompletion) {
    challenges.value.forEach((challenge) => {
      if (
        oldDistance < challenge.length &&
        mileageStore.totalChallengeKmByUser >= challenge.length
      ) {
        challengeName.value = challenge.name
        isCompleted.value = true
      }
    })
  }
}

onMounted(async () => {
  if (userStore.user) {
    try {
      getIconName(userStore.user.travelMethod)
      await mileageStore.getMileageByUser()
      await updateChallengeProgress(false)
    } catch (error) {
      console.log(error)
    }
  }
  loading.value = false
})
</script>

<style scoped>
.progress-bar {
  background-color: #e2e2e2;
}

.progress-bar > div,
.length-label {
  height: 30px;
}
</style>
