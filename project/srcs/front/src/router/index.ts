import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import EmailConfirmationPage from '@/views/EmailConfirmationPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ProfileOnboarding from '@/views/ProfileOnboarding.vue';
import HomePage from '@/views/Protected/HomePage.vue';
import ExplorePage from '@/views/Protected/ExplorePage.vue';
import MessagesPage from '@/views/Protected/MessagesPage.vue';
import NotificationsPage from '@/views/Protected/NotificationsPage.vue';
import ProfilePage from '@/views/Protected/ProfilePage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomePage,
      children: [
        {
          path: '',
          component: ExplorePage
        },
        {
          path: 'messages',
          component: MessagesPage
        },
        {
          path: 'notifications',
          component: NotificationsPage
        },
        {
          path: 'profile',
          component: ProfilePage
        },
      ]
    },
    {
      path: '/landing',
      name: 'landing',
      component: LandingPage,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
    },
    {
      path: '/confirm-email',
      name: 'email confirmation',
      component: EmailConfirmationPage,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/profile-onboarding',
      name: 'profile onboarding',
      component: ProfileOnboarding
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
})

export default router
