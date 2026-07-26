"use client";

import { useEffect, useRef, useState } from "react";

declare global {
  interface Window {
    YT?: typeof YT;
    onYouTubeIframeAPIReady?: () => void;
  }
}

/**
 * Thin wrapper around the YouTube IFrame Player API. Loads the API script
 * once, mounts a player into the given container id, and exposes basic
 * transport controls. The Sequencing Agent decides *what* plays; this hook
 * only concerns itself with *how* playback happens in the browser.
 */
export function useYoutubePlayer(containerId: string) {
  const playerRef = useRef<YT.Player | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (window.YT?.Player) {
      setReady(true);
      return;
    }

    const tag = document.createElement("script");
    tag.src = "https://www.youtube.com/iframe_api";
    document.body.appendChild(tag);

    window.onYouTubeIframeAPIReady = () => setReady(true);
  }, []);

  useEffect(() => {
    if (!ready || playerRef.current) return;
    playerRef.current = new window.YT!.Player(containerId, {
      height: "0",
      width: "0",
      playerVars: { autoplay: 0, controls: 0 },
    });
  }, [ready, containerId]);

  const loadVideo = (videoId: string) => playerRef.current?.loadVideoById(videoId);
  const play = () => playerRef.current?.playVideo();
  const pause = () => playerRef.current?.pauseVideo();
  const seekTo = (seconds: number) => playerRef.current?.seekTo(seconds, true);
  const setVolume = (v: number) => playerRef.current?.setVolume(Math.round(v * 100));

  return { ready, loadVideo, play, pause, seekTo, setVolume };
}
