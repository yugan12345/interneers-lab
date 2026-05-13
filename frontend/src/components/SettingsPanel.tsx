import React, { useEffect } from "react";
import "./SettingsPanel.css";

export type FontSize = "small" | "medium" | "large";
export type Density = "compact" | "comfortable";

export interface Settings {
  theme: "light" | "dark";
  fontSize: FontSize;
  density: Density;
  animations: boolean;
  pageSize: number;
}

export const defaultSettings: Settings = {
  theme: "dark",
  fontSize: "medium",
  density: "comfortable",
  animations: true,
  pageSize: 9,
};

/** Apply settings to the <html> element so CSS variables take effect globally */
export function applySettings(s: Settings) {
  const root = document.documentElement;

  // Theme
  root.setAttribute("data-theme", s.theme);

  // Font size
  const fontSizeMap: Record<FontSize, string> = {
    small: "13px",
    medium: "15px",
    large: "17px",
  };
  root.style.setProperty("--base-font-size", fontSizeMap[s.fontSize]);

  // Density
  const densityMap: Record<Density, string> = {
    compact: "12px",
    comfortable: "24px",
  };
  root.style.setProperty("--card-padding", densityMap[s.density]);
  root.style.setProperty(
    "--card-gap",
    s.density === "compact" ? "10px" : "16px"
  );

  // Animations
  root.style.setProperty(
    "--transition-speed",
    s.animations ? "300ms" : "0ms"
  );
  root.setAttribute("data-animations", s.animations ? "on" : "off");
}

interface Props {
  settings: Settings;
  onChange: (s: Settings) => void;
  onClose: () => void;
}

export default function SettingsPanel({ settings, onChange, onClose }: Props) {
  // Re-apply whenever settings change
  useEffect(() => {
    applySettings(settings);
  }, [settings]);

  function set<K extends keyof Settings>(key: K, value: Settings[K]) {
    onChange({ ...settings, [key]: value });
  }

  return (
    <div className="settings-overlay" onClick={onClose}>
      <div className="settings-panel" onClick={(e) => e.stopPropagation()}>
        <div className="settings-header">
          <h2>Settings</h2>
          <button className="settings-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="settings-body">
          {/* Appearance */}
          <div className="settings-section">
            <div className="settings-section-title">Appearance</div>

            <div className="settings-row">
              <span>Theme</span>
              <div className="settings-toggle-group">
                {(["light", "dark"] as const).map((t) => (
                  <button
                    key={t}
                    className={`settings-toggle ${settings.theme === t ? "active" : ""}`}
                    onClick={() => set("theme", t)}
                  >
                    {t === "light" ? "☀ Light" : "☾ Dark"}
                  </button>
                ))}
              </div>
            </div>

            <div className="settings-row">
              <span>Font size</span>
              <div className="settings-toggle-group">
                {(["small", "medium", "large"] as const).map((f) => (
                  <button
                    key={f}
                    className={`settings-toggle ${settings.fontSize === f ? "active" : ""}`}
                    onClick={() => set("fontSize", f)}
                  >
                    {f.charAt(0).toUpperCase() + f.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <div className="settings-row">
              <span>Density</span>
              <div className="settings-toggle-group">
                {(["compact", "comfortable"] as const).map((d) => (
                  <button
                    key={d}
                    className={`settings-toggle ${settings.density === d ? "active" : ""}`}
                    onClick={() => set("density", d)}
                  >
                    {d.charAt(0).toUpperCase() + d.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Behaviour */}
          <div className="settings-section">
            <div className="settings-section-title">Behaviour</div>

            <div className="settings-row">
              <span>Animations</span>
              <button
                className={`settings-switch ${settings.animations ? "on" : ""}`}
                onClick={() => set("animations", !settings.animations)}
              >
                <span className="settings-switch-thumb" />
              </button>
            </div>

            <div className="settings-row">
              <span>Products per page</span>
              <select
                className="settings-select"
                value={settings.pageSize}
                onChange={(e) => set("pageSize", Number(e.target.value))}
              >
                {[6, 9, 12, 18, 24].map((n) => (
                  <option key={n} value={n}>
                    {n}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="settings-footer">
          <button
            className="btn-secondary"
            onClick={() => onChange(defaultSettings)}
          >
            Reset to defaults
          </button>
        </div>
      </div>
    </div>
  );
}