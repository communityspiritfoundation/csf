<template>
  <v-container>
    <v-row class="mx-6" :fullscreen="mobile">
      <!-- Team Name -->
      <v-row align="center" class="my-2 px-5">
        <v-col align="center">
          <h1>{{ teamData.team_name }}</h1>
        </v-col>
        <EditTeamInfo />
      </v-row>
      <v-divider />

      <!-- Total Kilometres -->
      <v-row align="center" class="my-2">
        <v-icon
          :class="['mdi', 'ml-3 mt-1', getIconName(userStore.user!.travelMethod)]"
          size="52"
        />
        <v-col>
          <v-chip color="green" class="rounded text-h5"
            >{{ Math.round(mileageStore.totalKmByTeam * 100) / 100 }} KM</v-chip
          >
          <h3>TOTAL</h3>
        </v-col>
      </v-row>
      <v-divider />

      <!-- Invite Code -->
      <v-row align="center" class="my-2">
        <v-col>
          <h2>Invite Code</h2>
          <p class="invite-code">{{ teamData.invite_code }}</p>
        </v-col>
        <v-tooltip location="end">
          <template v-slot:activator="{ props }">
            <v-icon
              @click="copyInviteCode"
              v-bind="props"
              class="mdi mdi-clipboard-multiple-outline px-10"
              size="32px"
            />
          </template>
          <span>{{ copyHoverText }}</span>
        </v-tooltip>
      </v-row>
      <v-divider />

      <!-- User Events -->
      <v-container class="pa-0">
        <v-row id="pointer-cursor" class="my-2">
          <v-col class="" @click="isEventsVisible = !isEventsVisible">
            <h2>Users Events</h2>
          </v-col>
          <v-icon
            v-if="isEventsVisible"
            icon="mdi mdi-chevron-down"
            @click="isEventsVisible = !isEventsVisible"
            class="px-10"
            size="50px"
          />
          <v-icon
            v-else
            icon="mdi mdi-chevron-right"
            @click="isEventsVisible = !isEventsVisible"
            class="px-10"
            size="50px"
          />
        </v-row>
        <v-row v-if="isEventsVisible" class="mt-n4 mb-2">
          <v-col class="d-flex flex-wrap">
            <v-row class="py-2 pl-2">
              <div v-for="(item, index) in teamData.users_events" :key="index">
                <div class="rounded-pill bg-green px-3 py-0.5 mx-2">
                  <span class="text-white">{{ item }}</span>
                </div>
              </div>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
      <v-divider />

      <!-- Bio -->
      <v-container class="pa-0">
        <v-row id="pointer-cursor" class="my-2">
          <v-col @click="isBioVisible = !isBioVisible">
            <h2>Bio</h2>
          </v-col>
          <v-icon
            v-if="isBioVisible"
            icon="mdi mdi-chevron-down"
            @click="isBioVisible = !isBioVisible"
            class="px-10"
            size="50px"
          />
          <v-icon
            v-else
            icon="mdi mdi-chevron-right"
            @click="isBioVisible = !isBioVisible"
            class="px-10"
            size="50px"
          />
        </v-row>
        <v-row v-if="isBioVisible" class="mt-n4 mb-2">
          <v-col>
            <p>{{ teamData.bio }}</p>
          </v-col>
        </v-row>
      </v-container>
      <v-divider></v-divider>

      <!-- Daily Kilometres -->
      <v-container class="pa-0">
        <v-row align="start" id="pointer-cursor" class="my-2">
          <v-col @click="isDailyKmsVisible = !isDailyKmsVisible">
            <h2>Daily KMs</h2>
          </v-col>
          <v-icon
            v-if="isDailyKmsVisible"
            @click="isDailyKmsVisible = !isDailyKmsVisible"
            icon="mdi mdi-chevron-down"
            size="50px"
            class="px-10"
          />
          <v-icon
            v-else
            @click="isDailyKmsVisible = !isDailyKmsVisible"
            icon="mdi mdi-chevron-right"
            size="50px"
            class="px-10"
          />
        </v-row>
        <v-row v-if="isDailyKmsVisible" class="mt-n4 mb-2">
          <v-col>
            <MileageGraph :dataPoints="mileageStore.mileageByTeam" />
          </v-col>
        </v-row>
      </v-container>
      <v-divider />

      <!-- Leaderboard -->
      <v-container class="pa-0">
        <v-row
          align="start"
          @click="isLeaderboardVisible = !isLeaderboardVisible"
          id="pointer-cursor"
          class="my-2"
        >
          <v-col>
            <h2>Leaderboard</h2>
          </v-col>
          <v-icon
            v-if="isLeaderboardVisible"
            icon="mdi mdi-chevron-down"
            size="50px"
            class="px-10"
          />
          <v-icon v-else icon="mdi mdi-chevron-right" size="50px" class="px-10" />
        </v-row>
        <div v-if="isLeaderboardVisible" class="mx-12">
          <v-table fixed-header class="py-2">
            <thead>
              <tr>
                <th id="placeColumn" class="text-right">Place</th>
                <th id="nameColumn" class="text-left">Name</th>
                <th id="distanceColumn" class="text-right">Distance</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in teamData.leaderboard?.leaderboard" :key="entry.rank">
                <td v-if="entry.rank < 4" class="text-right text-subtitle-1">
                  <v-icon icon="mdi-trophy" size="25px" :class="getTrophyColour(entry.rank)" />
                  <span>{{ entry.rank }}</span>
                </td>
                <td v-if="entry.rank > 3" class="text-right text-subtitle-1">
                  <span>{{ entry.rank }}</span>
                </td>
                <td class="text-subtitle-1">
                  <span>{{ entry.username }}</span>
                </td>
                <td class="text-right text-subtitle-1">
                  {{ Math.round(entry.totalMileage * 100) / 100 }}
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </v-container>
      <v-divider />

      <!-- Sub-teams -->
      <v-container class="pa-0">
        <v-row align="start" class="my-2">
          <v-col id="pointer-cursor" @click="isSubTeamsVisible = !isSubTeamsVisible">
            <h2>Sub-Teams</h2>
          </v-col>
          <v-icon
            v-if="isSubTeamsVisible"
            icon="mdi mdi-chevron-down"
            @click="isSubTeamsVisible = !isSubTeamsVisible"
            size="50px"
            id="pointer-cursor"
            class="px-10"
          />
          <v-icon
            v-else
            icon="mdi mdi-chevron-right"
            @click="isSubTeamsVisible = !isSubTeamsVisible"
            size="50px"
            id="pointer-cursor"
            class="px-10"
          />
        </v-row>
        <v-row v-if="isSubTeamsVisible" class="my-2">
          <v-col cols="12" class="w-100" id="pointer-cursor">
            <SubTeams />
          </v-col>
        </v-row>
      </v-container>
      <v-divider />

      <v-divider class="mb-10" />
    </v-row>
  </v-container>

  <!-- Leave/Delete Team -->
  <v-row justify="center" class="ma-5">
    <ConfirmButton
      v-if="userStore.user!.teamAdmin"
      :action="'delete'"
      :object="'team'"
      :use-done-for-button="false"
      :loading="loading"
      @handle-confirm="deleteTeam"
    />
    <ConfirmButton
      v-else
      :action="'leave'"
      :object="'team'"
      :use-done-for-button="false"
      :loading="loading"
      @handle-confirm="removeTeam"
    />
  </v-row>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'
import EditTeamInfo from './EditTeamInfo.vue'
import SubTeams from './SubTeams.vue'
import MileageGraph from '../MileageGraph.vue'
import ConfirmButton from '@/components/ConfirmButton.vue'
const { mobile } = useDisplay()
import { useTeamStore } from '@/stores/team'
import { useUserStore } from '@/stores/user'
import { AxiosError } from 'axios'
import { notify } from '@kyvg/vue3-notification'
import { useMileageStore } from '@/stores/mileage'
import type { UserLeaderboard } from '@/types/mileage'

const teamStore = useTeamStore()
const userStore = useUserStore()
const loading = ref(false)
const mileageStore = useMileageStore()

mileageStore.getMileageByTeam()

onMounted(async () => {
  if (userStore.user!.teamId)
    await teamStore.getTeam(userStore.user!.teamId).catch((error: AxiosError | any) => {
      if (error instanceof AxiosError && error.response) {
        notify({
          title: 'Get Team',
          type: 'error',
          text: 'Get Team Error'
        })
      }
    })
  if (userStore.user!.teamId) {
    teamData.value.leaderboard = (await mileageStore.getLeaderboard({
      type: 'team',
      teamId: userStore.user!.teamId
    })) as UserLeaderboard
  }
})
const deleteTeam = () => {
  loading.value = true
  teamStore.deleteTeam().catch((error: AxiosError | any) => {
    if (error instanceof AxiosError && error.response) {
      notify({
        title: 'Delete Team',
        type: 'error',
        text: 'Delete Team Error'
      })
    }
  })
}
const removeTeam = () => {
  loading.value = true
  teamStore.removeTeam().catch((error: AxiosError | any) => {
    if (error instanceof AxiosError && error.response) {
      notify({
        title: 'Remove Team',
        type: 'error',
        text: 'Remove Team Error'
      })
    }
  })
}

const teamData = ref({
  team_name: teamStore.team ? teamStore.team.name : '',
  total_kilometres: 0,
  invite_code: teamStore.team ? teamStore.team.joinCode : '',
  bio: teamStore.team ? teamStore.team.bio : '',
  daily_kms: [],
  sub_teams: [],
  leaderboard: {} as UserLeaderboard | undefined,
  users_events: teamStore.team ? teamStore.team.usersEvents : []
})

watch(
  () => teamStore.team,
  (newTeam) => {
    // Update the teamData when the team value changes
    if (newTeam) {
      teamData.value.team_name = newTeam.name
      teamData.value.bio = newTeam.bio
      teamData.value.invite_code = newTeam.joinCode
    }
  }
)

const isBioVisible = ref(false)
const isDailyKmsVisible = ref(true)
const isSubTeamsVisible = ref(false)
const isLeaderboardVisible = ref(false)
const isEventsVisible = ref(true)

const copyHoverText = ref('Copy to Clipboard')

const copyInviteCode = () => {
  navigator.clipboard.writeText(teamData.value.invite_code)
  copyHoverText.value = 'Copied!'

  setTimeout(() => {
    copyHoverText.value = 'Copy Invite Code'
  }, 2000)
}

const getIconName = (medium: string) => {
  switch (medium) {
    case 'RUNNING':
      return 'mdi-run-fast'
    case 'WHEELING':
      return 'mdi-wheelchair-accessibility'
    case 'WALKING':
      return 'mdi-walk'
  }
}

const getTrophyColour = (rank: number) => {
  switch (rank) {
    case 1:
      return 'text-yellow-darken-1'
    case 2:
      return 'text-blue-grey-lighten-1'
    default:
      return 'text-orange-darken-1'
  }
}
</script>

<style scoped>
.totalKms {
  font-size: 1.5rem;
}

.mdi-clipboard-multiple-outline:active {
  translate: 0px 2px;
}

#pointer-cursor {
  cursor: pointer;
}

.invite-code {
  font-size: 0.7rem;
}

#placeColumn {
  width: 80px;
}

#nameColumn {
  width: auto;
}

#distanceColumn {
  width: 33%;
}
</style>
