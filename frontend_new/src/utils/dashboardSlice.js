// src/redux/slices/dashboardSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  prompt: '',
  layout: null,
};

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    setPrompt: (state, action) => {
      state.prompt = action.payload;
    },
    setLayout: (state, action) => {
      state.layout = action.payload;
    },
    resetDashboard: () => initialState,
  },
});

export const { setPrompt, setLayout, resetDashboard } = dashboardSlice.actions;
export default dashboardSlice.reducer;
