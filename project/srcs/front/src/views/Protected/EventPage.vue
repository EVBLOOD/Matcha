<script setup lang="ts">
    import { ref, computed } from 'vue';

    const activeTab = ref('all');
    const events = ref([
        { type: 'sender', from: '@idkart', to: '@gkleier', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'pending' },
        { type: 'receiver', from: '@gkleier', to: '@idkart', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'pending' },
        { type: 'sender', from: '@idkart', to: '@gkleier', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'accepted' },
        { type: 'receiver', from: '@gkleier', to: '@idkart', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'declined' },
    ])

    const filteredEvents = computed(() => {
        if (activeTab.value === 'all')
            return events.value
        if (activeTab.value === 'sent') 
            return events.value.filter(e => e.type === 'sender')
        if (activeTab.value === 'received') 
            return events.value.filter(e => e.type === 'receiver')
        return events.value
    })

    function setActive(tab: string) {
        activeTab.value = tab;
    }
    
</script>

<template>
    <div class="page">
        <div class="content">
            <nav class="tab">
                <div class="link" :class="{ active: activeTab == 'all' }" @click="setActive('all')">All Events</div>
                <div class="link" :class="{ active: activeTab == 'sent' }" @click="setActive('sent')">Event sent</div>
                <div class="link" :class="{ active: activeTab == 'received' }" @click="setActive('received')">Event received</div>
            </nav>

            <div class="events">
                <div v-for="(event, index) in filteredEvents" :key="index" class="event-card">
                    <div class="users">
                        <span class="user">
                            <img src="/img/profilePictureDemo.png" :alt="event.from" width="45" height="45" />
                            <p>{{ event.from }}</p>
                        </span>
                        <span>
                            <img src="/img/arrow.svg"/>
                        </span>
                        <span class="user">
                            <img src="/img/profilePictureDemo.png" :alt="event.to" width="45" height="45" />
                            <p>{{ event.to }}</p>
                        </span>
                    </div>
                    <div class="details">
                        <div class="date_location">
                            <div class="info">
                                <img src="/img/CalendarEvent.svg" alt="date" />
                                <p>{{ event.date }}</p>
                            </div>
                            <div class="info">
                                <img src="/img/MapEvent.svg" alt="location" />
                                <p>{{ event.location }}</p>
                            </div>
                        </div>
                        <div class="info">
                            <img src="/img/MessageEvent.svg" alt="message" />
                            <p>{{ event.message }}</p>
                        </div>
                    </div>
                    <div class="status" v-if="event.type === 'sender'">
                        <span class="pending" v-if="event.status === 'pending'">
                            <img src="/img/MessageEvent.svg" alt="pending" />
                            <p>Pending</p>
                        </span>
                        <span class="accepted" v-else-if="event.status === 'accepted'">
                            <img src="/img/MessageEvent.svg" alt="pending" />
                            <p>Accepted</p>
                        </span>
                        <span class="declined" v-else-if="event.status === 'declined'">
                            <img src="/img/MessageEvent.svg" alt="declined" />
                            <p>Declined</p>
                        </span>
                    </div>
                    <div class="confirmation" v-if="event.type === 'receiver'">
                        <button v-if="event.status === 'pending'" class="btn-decline">
                            <img src="/img/DeclineEvent.svg" alt="decline" />
                        </button>
                        <button v-if="event.status === 'pending'" class="btn-accept">
                            <img src="/img/AcceptEvent.svg" alt="accept" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .page{
        padding: 2%;
        display: flex;
        flex-direction: column;
        gap: 0.5%;
    }
    
    .content {
        display: flex;
        flex-direction: column;
    }

    nav {
        display: flex;
        gap: 25px;
        margin-bottom: 30px;
    }

    .tab{
        width: 100%;
    }

    .link {
        cursor: pointer;
        text-decoration: none;
        color: $text-color;
        padding-bottom: 5px;
        font-weight: 600;
        &:hover {
            border-style: solid;
            border-width: 0px 0px 5px 0px;
            border-color: $border-color-hover;
        }
        &.active {
            border-style: solid;
            border-width: 0px 0px 5px 0px;
            border-color: $border-color-active;
        }
    }

    .events {
        display: flex;
        flex-direction: column;
        gap: 1rem;

        .event-card {
            background: $components-background-color;
            padding: 3rem 2rem;
            border-radius: 8px;
            display: grid;
            grid-template-columns: max-content 1fr min-content;
            align-items: center;
            // justify-content: space-between;

            .users {
                display: flex;
                gap: 0.5rem;
                align-items: center;
                

                .user {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 0.25rem;

                    img {
                        border-radius: 50%;
                    }
                }
            }

            .details {
                // flex: 1;
                margin-left: 1rem;
                display: flex;
                gap: 20%;
                // width: 100%;
                .info {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }

                .date_location{

                }

            }

            .status {
                span {
                    white-space: nowrap;
                    padding: 10px 15px;
                    border-radius: 20px;
                    background: $components-background-color;
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-weight: 600;
                }
                .accepted {
                    background: #E2BDF6;
                    color: #382343;
                }
            }

            .confirmation {
                display: flex;

                button{
                    background: none;
                    border: none;
                    cursor: pointer;
                    margin-left: 10px;
                    border-radius: 10px;
                    height: 60px;
                    width: 60px;
                    transition: 0.3s;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .btn-accept {
                    background-color: #BB85D7;
                }
                
                .btn-decline {
                    background: $components-background-color;
                }

                button:hover {
                    filter: brightness(0.9);
                    transition: 0.3s;
                }
            }
        }
    }

</style>