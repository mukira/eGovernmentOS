#ifndef CHROME_BROWSER_UI_WEBUI_NXTSCAPE_FIRST_RUN_H_
#define CHROME_BROWSER_UI_WEBUI_NXTSCAPE_FIRST_RUN_H_

#include <memory>
#include <string>
#include <utility>

#include "base/memory/ref_counted_memory.h"
#include "chrome/browser/profiles/profile.h"
#include "content/public/browser/url_data_source.h"
#include "content/public/browser/web_ui.h"
#include "content/public/browser/web_ui_controller.h"
#include "content/public/browser/webui_config.h"
#include "services/network/public/mojom/content_security_policy.mojom.h"
#include "url/gurl.h"

class UFRDataSource : public content::URLDataSource {
public:
  UFRDataSource() = default;
  UFRDataSource(const UFRDataSource &) = delete;
  UFRDataSource &operator=(const UFRDataSource &) = delete;

  // URLDataSource implementation:
  std::string GetSource() override;
  std::string GetMimeType(const GURL &url) override;
  std::string
  GetContentSecurityPolicy(network::mojom::CSPDirectiveName directive) override;
  void StartDataRequest(const GURL &url,
                        const content::WebContents::Getter &wc_getter,
                        GotDataCallback callback) override;
};

// Implementation of UFRDataSource
std::string UFRDataSource::GetSource() { return "egovernmentos-first-run"; }

std::string UFRDataSource::GetMimeType(const GURL &url) { return "text/html"; }

std::string UFRDataSource::GetContentSecurityPolicy(
    network::mojom::CSPDirectiveName directive) {
  if (directive == network::mojom::CSPDirectiveName::ScriptSrc)
    return "'unsafe-inline'";
  if (directive == network::mojom::CSPDirectiveName::StyleSrc)
    return "'unsafe-inline' https://fonts.googleapis.com";
  if (directive == network::mojom::CSPDirectiveName::FontSrc)
    return "https://fonts.gstatic.com";
  if (directive == network::mojom::CSPDirectiveName::ImgSrc)
    return "'self' data:";
  return std::string();
}

void UFRDataSource::StartDataRequest(
    const GURL &url, const content::WebContents::Getter &wc_getter,
    GotDataCallback callback) {
  std::string source = R"(
<!DOCTYPE html>
<html lang="en">

<head>
    <title>eGovernmentOS: First Run</title>
    <meta charset="UTF-8">
    <meta name="color-scheme" content="light dark">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg version='1.1' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1024 1024'%3E%3Cstyle%3E.st0%7Bfill:none%7D.st1%7Bfill:none;stroke:%231266F1;stroke-width:209;stroke-miterlimit:10%7D%3C/style%3E%3Cg%3E%3Ccircle class='st0' cx='513.3' cy='510.8' r='454.9'/%3E%3Ccircle class='st1' cx='758.2' cy='988.4' r='411.5'/%3E%3Ccircle class='st1' cx='262' cy='81.4' r='411.5'/%3E%3C/g%3E%3C/svg%3E">
    <style>
        @import url(chrome://resources/css/text_defaults_md.css);

        :root {
            --bg: #FAF7F3;
            --text: #1F1D1B;
            --muted: #6B7280;
            --border: #E8E2DA;
            --card: #FFFFFF;
            --accent: #1266F1;
            --cta: #231F1A;
            --link: #1F2937;
            --chip-bg: #F1F4F8;
            --chip-border: #E2E8F0;
            --chip-text: #0F172A;
            --kbd-bg: #F5F7FA;
            --kbd-border: #E5E7EB;
            --kbd-border2: #DBDEE3;
            --kbd-text: #111827;
            --note-bg: #F9FAFB;
            --note-border: #D6D3CE;
            --note-text: #374151;
            --badge-bg: #FFFFFFAA;
            --badge-border: var(--border);
            --badge-text: #4B5563;
            --linkpill-bg: var(--card);
            --linkpill-text: var(--text);
            --social-icon: #6b7280;
            --shadow-lg: 0 24px 40px -20px rgba(0, 0, 0, .12);
            --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.06);
            --accent-purple: #a78bfa;
            --accent-teal: #22d3ee;
            --accent-amber: #f59e0b;
            --feature-card-h: 128px;
        }

        /* Use Roboto everywhere */
        #titanium-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            /* Background handled by canvas draw, but set fallback */
            background: #0b0f14;
        }
        html {
            color: var(--text);
            /* Make transparent so canvas shows through if needed, though canvas is fixed */
            background: transparent;
            line-height: 1.6;
            font-family: "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
            font-size: 16px;
        }

        a {
            color: var(--link);
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        h2 {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: .1px;
        }

        p {
            margin: 0;
        }

        ul,
        ol {
            padding-left: 1.25rem;
            margin: .5rem 0;
        }

        code {
            background: var(--chip-bg);
            padding: .2rem .5rem;
            border: 1px solid var(--chip-border);
            border-radius: .5rem;
            font-size: .875rem;
            color: var(--chip-text)
        }

        kbd {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background: var(--kbd-bg);
            border: 1px solid var(--kbd-border);
            border-bottom-color: var(--kbd-border2);
            border-radius: .35rem;
            padding: .15rem .4rem;
            font-size: .85rem;
            color: var(--kbd-text)
        }

        /* Base section layout and consistent vertical rhythm */
        section {
            width: 64rem;
            max-width: 92%;
            margin: 0 auto 2.5rem;
            padding-top: 0;
        }

        /* Add uniform top spacing only between subsequent sections */
        /* Default spacing between sections */
        section+section {
            padding-top: 2.75rem;
        }

        /* Tighter spacing from hero to first content section */
        .hero+section {
            padding-top: 1.25rem;
        }

        /* Hero */
        .hero {
            text-align: center;
            padding: 4.5rem 0 1.5rem 0;
        }

        .hero .subtitle {
            font-size: 0.875rem;
            font-weight: 500;
            background: linear-gradient(to bottom, #93C5FD 10%, #3B82F6 45%, #93C5FD 50%, #3B82F6 55%, #93C5FD 90%);
            background-size: 100% 200%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
            filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.5));
        }

        .hero h1 {
            font-family: inherit;
            font-size: 4.5rem;
            line-height: 1.15;
            margin: 0 0 1.75rem;
            background: linear-gradient(to bottom, #FFFFFF 10%, #A0A0A0 45%, #FFFFFF 50%, #A0A0A0 55%, #FFFFFF 90%);
            background-size: 100% 200%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: var(--text);
            letter-spacing: -1px;
            font-weight: 600;
            filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.5));
        }

        .hero .accent {
            background: linear-gradient(to bottom, #60A5FA 10%, #1E40AF 45%, #60A5FA 50%, #1E40AF 55%, #60A5FA 90%);
            background-size: 100% 200%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: var(--accent);
            font-style: normal;
            font-weight: 600;
            filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.5));
        }

        .hero p {
            font-size: 1.05rem;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.8);
            margin: 0 auto 2rem;
            max-width: 900px;
            font-weight: 300;
        }

        .subtle {
            color: var(--muted);
            font-size: .95rem;
            margin-top: .75rem;
        }

        .badge-row {
            display: flex;
            justify-content: center;
            gap: .5rem;
            margin: .75rem 0 2.5rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: .8rem;
            padding: .6rem 1.5rem;
            font-size: 0.95rem;
            font-weight: 500;
            color: #fff;
            position: relative;
            z-index: 0;
            border-radius: 999px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .badge::before {
            content: '';
            position: absolute;
            inset: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent 0%, transparent 60%, #22d3ee 85%, #ffffff 95%, transparent 100%);
            animation: rotate 4s linear infinite;
            z-index: -2;
        }

        .badge::after {
            content: '';
            position: absolute;
            inset: 1.5px;
            /* Lighter, glossier gradient */
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.15) 0%, rgba(11, 18, 32, 0.6) 35%, rgba(11, 18, 32, 0.9) 100%);
            backdrop-filter: blur(24px);
            border-radius: 999px;
            z-index: -1;
            /* Stronger top reflection for gloss */
            box-shadow: inset 0 1px 0.5px rgba(255, 255, 255, 0.6), inset 0 -1px 0.5px rgba(0, 0, 0, 0.4);
        }

        /* Buttons */
        .actions {
            margin-top: 1rem
        }

        /* Remove stray space when no buttons are present */
        .hero .actions:empty {
            display: none
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: .5rem;
            padding: .8rem 1rem;
            border-radius: 999px;
            border: 1px solid transparent;
            font-weight: 600;
            text-decoration: none
        }

        .btn .icon {
            display: inline-flex;
            width: 18px;
            height: 18px
        }

        .btn .icon svg {
            width: 18px;
            height: 18px
        }

        .btn-dark {
            background: var(--cta);
            color: #fff;
            box-shadow: 0 8px 18px rgba(0, 0, 0, .18);
        }

        .btn-outline {
            background: transparent;
            color: var(--text);
            border-color: var(--border);
        }

        .btn-accent {
            /* Glassy Blue Button */
            background: linear-gradient(135deg, rgba(18, 102, 241, 0.85), rgba(18, 102, 241, 0.65)) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.3);
            color: #fff;
            box-shadow: 0 8px 32px 0 rgba(18, 102, 241, 0.4), inset 0 0 0 1px rgba(255, 255, 255, 0.2);
        }

        .btn-accent:hover {
            filter: brightness(1.05)
        }

        .btn+.btn {
            margin-left: .5rem
        }

        /* Section headers */
        .section-head {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 0 1rem;
        }

        .section-head .label {
            font-family: inherit;
            font-size: 1.7rem;
            color: var(--text);
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .section-head .label svg {
            filter: drop-shadow(0 0 10px var(--accent)) drop-shadow(0 0 20px var(--accent));
        }

        .section-head .label .accent {
            color: var(--accent);
            font-style: normal
        }

 /* Light cards and groups with White Glassmorphism & Glistening Shine */
 .group,.card,.banner{background:linear-gradient(135deg,rgba(255,255,255,0.96),rgba(255,255,255,0.9))!important;backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border:1.5px solid rgba(255,255,255,1);border-radius:1rem;padding:1.15rem 1.25rem;box-shadow:0 12px 40px 0 rgba(0,0,0,0.15),inset 0 0 15px rgba(255,255,255,0.8),inset 0 0 0 1px rgba(255,255,255,0.5);color:#000000!important;position:relative;overflow:hidden;}
 .group::before,.card::before,.banner::before{content:'';position:absolute;top:0;left:-150%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);transform:skewX(-20deg);animation:card-shine 3s forwards;pointer-events:none;}
 @keyframes card-shine{0%{left:-150%;}30%{left:150%;}100%{left:150%;}}
 .group+.group{margin-top:1rem;}

        .title {
            font-size: 1.15rem;
            color: #000000;
            margin-bottom: .5rem;
        }

        /* Legacy CTA (kept for quick link outside buttons) */
        .cta {
            display: inline-block;
            margin-top: .75rem;
            padding: .85rem 1.25rem;
            border-radius: 999px;
            color: #fff;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            box-shadow: 0 12px 26px rgba(99, 102, 241, .28);
            font-weight: 700
        }

        .cta:hover {
            filter: brightness(1.05);
        }

        /* Cards grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
            gap: 1.25rem;
        }

        .grid.features {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            column-gap: 1.5rem;
            row-gap: 2rem;
            grid-auto-flow: row;
        }

        @media (max-width: 720px) {
            .grid.features {
                grid-template-columns: 1fr;
                row-gap: 1.25rem;
            }

            .features .card {
                height: auto;
                padding: 1rem 1.15rem
            }
        }

        .card h3,.banner .label {
            margin: .15rem 0 .6rem;
            font-size: 1.06rem;
            color: #000000!important;
            font-weight: 700;
        }

        .note {
            margin-top: .7rem;
            font-size: .92rem;
            color: var(--note-text);
            border: 1px dashed var(--note-border);
            background: var(--note-bg);
            padding: .6rem .75rem;
            border-radius: .5rem
        }

        /* Heading icons */
        .hicon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            margin-right: .55rem;
            vertical-align: middle
        }

        .hicon.import {
            color: var(--accent-purple)
        }

        .hicon.key {
            color: var(--accent-teal)
        }

        .hicon.keyboard {
            color: var(--accent-amber)
        }

        .hicon.check {
            color: #02b302
        }

        .hicon svg {
            width: 22px;
            height: 22px;
            fill: currentColor
        }

        /* Banner */
        .banner {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1rem 1.25rem;
            color: var(--text);
            text-align: left;
            box-shadow: var(--shadow-lg)
        }

        .banner .label {
            display: flex;
            align-items: center;
            font-weight: 700;
        }

        /* Features cards */
        .features .card {
            height: var(--feature-card-h);
            /* Inherit glistening box-shadow from .card, do not override with shadow-md */
            padding: .7rem 1rem
        }

        .features .card h3 {
            margin: .05rem 0 .25rem;
            line-height: 1.28
        }

        .features .card p {
            line-height: 1.45
        }

        .features .card p+p {
            margin-top: .25rem !important
        }

        /* Icons for feature cards use accent color */
        .features .card .hicon {
            color: var(--accent)
        }

        .muted {
            color: #4b5563 !important;
        }

        .examples {
            margin-top: .75rem
        }

        .codebox {
            display: block;
            margin-top: .5rem;
            padding: .7rem .8rem;
            border-radius: .6rem;
            background: var(--chip-bg);
            border: 1px solid var(--chip-border);
            color: var(--chip-text);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: .9rem
        }

        /* Links row */
        .links a {
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            margin: .25rem .35rem;
            padding: .55rem .9rem;
            background: var(--linkpill-bg);
            border: 1px solid var(--border);
            border-radius: .7rem;
            color: var(--linkpill-text);
            box-shadow: 0 12px 24px -20px rgba(0, 0, 0, .15)
        }

        .links a:hover {
            background: var(--linkpill-bg);
            filter: brightness(1.03)
        }

        .links a .icon {
            display: inline-flex;
            width: 18px;
            height: 18px;
            color: var(--social-icon);
        }

        .links a .icon svg {
            width: 18px;
            height: 18px;
            fill: currentColor
        }

        .titanium {
            background: linear-gradient(to bottom, #FFFFFF 10%, #A0A0A0 45%, #FFFFFF 50%, #A0A0A0 55%, #FFFFFF 90%);
            background-size: 100% 200%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: #fff;
            filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.5));
        }

        @keyframes rotate {
            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }

        @keyframes shimmer {
            0% {
                background-position: 200% 0;
            }

            100% {
                background-position: -200% 0;
            }
        }

        @media(prefers-color-scheme:dark) {
            :root {
                --bg: #0b0f14;
                --text: #e5e7eb;
                --muted: #94a3b8;
                --border: #1f2a3a;
                --card: #101723;
                --cta: #161A23;
                --accent: #1266f1;
                --link: #9aa1ff;
                --chip-bg: #0b1220;
                --chip-border: #1f2937;
                --chip-text: #e5e7eb;
                --kbd-bg: #0b1220;
                --kbd-border: #1f2937;
                --kbd-border2: #1b2432;
                --kbd-text: #e5e7eb;
                --note-bg: #0b1220;
                --note-border: #273144;
                --note-text: #cbd5e1;
                --badge-bg: rgba(255, 255, 255, .08);
                --badge-border: #2a3342;
                --badge-text: #cbd5e1;
                --linkpill-bg: #101723;
                --linkpill-text: #e5e7eb;
                --social-icon: #9ca3af;
                --shadow-lg: 0 24px 40px -20px rgba(0, 0, 0, .6);
                --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.5);
                --accent-purple: #a78bfa;
                --accent-teal: #22d3ee;
                --accent-amber: #f59e0b;
            }
        }
    </style>
    <base target="_blank">
</head>

<body>
    <section class="hero">
        <div class="badge-row">
            <span class="badge"><svg version="1.1" xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" width="42" height="42"
                    style="enable-background:new 0 0 1024 1024;" xml:space="preserve">
                    <style type="text/css">
                        .st0 {
                            fill: none;
                        }

                        .st1 {
                            clip-path: url(#SVGID_3_);
                            fill: none;
                            stroke: #fff;
                            stroke-width: 209;
                            stroke-miterlimit: 10;
                        }

                        .st2 {
                            clip-path: url(#SVGID_5_);
                            fill: none;
                            stroke: #fff;
                            stroke-width: 209;
                            stroke-miterlimit: 10;
                        }
                    </style>
                    <g>
                        <g>
                            <circle id="SVGID_1_" class="st0" cx="513.3" cy="510.8" r="454.9" />
                        </g>
                        <g>
                            <g>
                                <defs>
                                    <circle id="SVGID_2_" cx="513.3" cy="510.8" r="454.9" />
                                </defs>
                                <clipPath id="SVGID_3_">
                                    <use xlink:href="#SVGID_2_" style="overflow:visible;" />
                                </clipPath>
                                <circle class="st1" cx="758.2" cy="988.4" r="411.5" />
                            </g>
                        </g>
                        <g>
                            <g>
                                <defs>
                                    <circle id="SVGID_4_" cx="513.3" cy="510.8" r="454.9" />
                                </defs>
                                <clipPath id="SVGID_5_">
                                    <use xlink:href="#SVGID_4_" style="overflow:visible;" />
                                </clipPath>
                                <circle class="st2" cx="262" cy="81.4" r="411.5" />
                            </g>
                        </g>
                    </g>
                </svg><span class="titanium">eGovernment OS</span></span>
        </div>
        <p class="subtitle">See Everything. Own Everything. Leak Nothing.</p>
        <h1>The Operating System for Modern Sovereign Governments</h1>
        <p>Address your toughest challenges with AI designed for government: coordinate departments automatically,
            process sensitive data securely, and eliminate repetitive tasks. eGovernmentOS delivers AI you can actually
            use, from the President's office to the border post.</p>
        <div class="actions">
        </div>
    </section>

    <section>
        <div class="section-head"><span class="label">🚀 <span class="titanium">Getting Started</span></span></div>
        <div style="text-align:center;">
            <a class="btn btn-accent" href="https://docs.deepintelgroup.com/onboarding">Quick start guide</a>
        </div>

        <div class="grid" style="margin-top:1rem;">
            <div class="card">
                <h3>
                    <span class="hicon import" aria-hidden="true">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                            <path
                                d="M5 20h14v-2H5v2zm7-16c.55 0 1 .45 1 1v6.17l2.59-2.58 1.41 1.41L12 14.59 6.99 10l1.41-1.41L11 11.17V5c0-.55.45-1 1-1z" />
                        </svg>
                    </span>
                    Step 1: Import your data from Chrome
                </h3>
                <ol>
                    <li>Navigate to <a href="chrome://settings/importData"><code>chrome://settings/importData</code></a>
                    </li>
                    <li>Click "Import"</li>
                    <li>Follow the prompts and choose "Always allow" when asked to import everything at once</li>
                </ol>
            </div>
            <div class="card">
                <h3>
                    <span class="hicon key" aria-hidden="true">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
                            <path
                                d="M420-680q0-33 23.5-56.5T500-760q33 0 56.5 23.5T580-680q0 33-23.5 56.5T500-600q-33 0-56.5-23.5T420-680ZM500 0 320-180l60-80-60-80 60-85v-47q-54-32-87-86.5T260-680q0-100 70-170t170-70q100 0 170 70t70 170q0 67-33 121.5T620-472v352L500 0ZM340-680q0 56 34 98.5t86 56.5v125l-41 58 61 82-55 71 75 75 40-40v-371q52-14 86-56.5t34-98.5q0-66-47-113t-113-47q-66 0-113 47t-47 113Z" />
                        </svg>
                    </span>
                    Step 2: BYOK (Bring Your Own Keys)
                </h3>
                <p class="muted">You have full control over your AI models!</p>
                <p class="muted" style="margin-top:.35rem">Navigate to <a
                        href="chrome://settings/egovernmentos"><code>chrome://settings/egovernmentos</code></a> to
                    configure
                    your own API keys for various providers.</p>
                <div class="note">Note: You can even run everything locally using Ollama!</div>
            </div>
        </div>

        <div class="banner" style="margin-top:1.1rem;">
            <div class="label">
                <span class="hicon check" aria-hidden="true">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                        fill="#02b302">
                        <path
                            d="m381-240 424-424-57-56-368 367-169-170-57 57 227 226Zm0 113L42-466l169-170 170 170 366-367 172 168-538 538Z" />
                    </svg>
                </span>
                Step 3: All done!
            </div>
            <div class="muted" style="margin-top:.4rem">Your ready to use eGovernmentOS, have fun! This page can be
                always accessed again at <a
                    href="chrome://egovernmentos-first-run"><code>chrome://egovernmentos-first-run</code></a></div>
        </div>
    </section>

    <section>
        <div class="section-head"><span class="label">✨ <span class="titanium">Key Features</span></span></div>
        <div class="grid features" style="margin-top:1rem;">
            <div class="card">
                <h3>
                    <span class="hicon feature-globe" aria-hidden="true">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                            fill="#1266f1">
                            <path
                                d="M480-80q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-155.5t86-127Q252-817 325-848.5T480-880q83 0 155.5 31.5t127 86q54.5 54.5 86 127T880-480q0 82-31.5 155t-86 127.5q-54.5 54.5-127 86T480-80Zm0-82q26-36 45-75t31-83H404q12 44 31 83t45 75Zm-104-16q-18-33-31.5-68.5T322-320H204q29 50 72.5 87t99.5 55Zm208 0q56-18 99.5-55t72.5-87H638q-9 38-22.5 73.5T584-178ZM170-400h136q-3-20-4.5-39.5T300-480q0-21 1.5-40.5T306-560H170q-5 20-7.5 39.5T160-480q0 21 2.5 40.5T170-400Zm216 0h188q3-20 4.5-39.5T580-480q0-21-1.5-40.5T574-560H386q-3 20-4.5 39.5T380-480q0 21 1.5 40.5T386-400Zm268 0h136q5-20 7.5-39.5T800-480q0-21-2.5-40.5T790-560H654q3 20 4.5 39.5T660-480q0 21-1.5 40.5T654-400Zm-16-240h118q-29-50-72.5-87T584-782q18 33 31.5 68.5T638-640Zm-234 0h152q-12-44-31-83t-45-75q-26 36-45 75t-31 83Zm-200 0h118q9-38 22.5-73.5T376-782q-56 18-99.5 55T204-640Z" />
                        </svg>
                    </span>
                    Natural-Language Specialists
                </h3>
                <p class="muted">Tell eGovernmentOS what to do in plain English: it clicks, types, and navigates for
                    you. No coding, no setup.</p>
                <p class="muted">Example: "Copy these LinkedIn contacts to a Google Sheet."</p>
            </div>
            <div class="card">
                <h3>
                    <span class="hicon feature-split" aria-hidden="true">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                            fill="#1266f1">
                            <path
                                d="M600-160v-80h160v-480H600v-80h160q33 0 56.5 23.5T840-720v480q0 33-23.5 56.5T760-160H600ZM440-80v-80H200q-33 0-56.5-23.5T120-240v-480q0-33 23.5-56.5T200-800h240v-80h80v800h-80Zm320-640v480-480Z" />
                        </svg>
                    </span>
                    Split-View AI on Any Page
                </h3>
                <p class="muted">Open ChatGPT, Claude, or Gemini alongside any website. Get help while you work:
                    summarize articles, draft responses, or analyze data without switching tabs.</p>
            </div>
            <div class="card">
                <h3>
                    <span class="hicon feature-private" aria-hidden="true">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                            fill="#1266f1">
                            <path
                                d="M240-80q-33 0-56.5-23.5T160-160v-400q0-33 23.5-56.5T240-640h40v-80q0-83 58.5-141.5T480-920q83 0 141.5 58.5T680-720v80h40q33 0 56.5 23.5T800-560v400q0 33-23.5 56.5T720-80H240Zm0-80h480v-400H240v400Zm240-120q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM360-640h240v-80q0-50-35-85t-85-35q-50 0-85 35t-35 85v80ZM240-160v-400 400Z" />
                        </svg>
                    </span>
                    Private by Default
                </h3>
                <p class="muted">Run AI locally with Ollama or bring your own API keys. Your data never leaves your
                    machine unless you choose.</p>
            </div>
            <div class="card">
                <h3>
                    <span class="hicon feature-ea" aria-hidden="true">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                            fill="#1266f1">
                            <path
                                d="M360-390q-21 0-35.5-14.5T310-440q0-21 14.5-35.5T360-490q21 0 35.5 14.5T410-440q0 21-14.5 35.5T360-390Zm240 0q-21 0-35.5-14.5T550-440q0-21 14.5-35.5T600-490q21 0 35.5 14.5T650-440q0 21-14.5 35.5T600-390ZM480-160q134 0 227-93t93-227q0-24-3-46.5T786-570q-21 5-42 7.5t-44 2.5q-91 0-172-39T390-708q-32 78-91.5 135.5T160-486v6q0 134 93 227t227 93Zm0 80q-83 0-156-31.5T197-197q-54 54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 127 85.5T480-80Zm-54-715q42 70 114 112.5T700-640q14 0 27-1.5t27-3.5q-42-70-114-112.5T480-800q-14 0-27 1.5t-27 3.5ZM177-581q51-29 89-75t57-103q-51 29-89 75t-57 103Zm249-214Zm-103 36Z" />
                        </svg>
                    </span>
                    Your Executive Assistant
                </h3>
                <p class="muted">Check email, schedule meetings, draft responses: all from the sidebar. Connect Gmail,
                    Calendar, Notion, and more with one-click MCP integration.</p>
            </div>
        </div>
    </section>



    <section>
        <div class="section-head"><span class="label">🤝 <span class="titanium">Join our community</span></span></div>
        <div class="links" style="text-align:center; margin-top:1rem;">
            <a href="https://discord.gg/25Ur5Ss7" target="_blank">
                <span class="icon">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z">
                        </path>
                    </svg>
                </span>
                Discord
            </a>
            <a href="https://join.slack.com/t/egovermentos/shared_invite/zt-3m4b9vojq-e3fLMujKjn7EU1firgS5nw" target="_blank">
                <span class="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" aria-label="Slack" role="img" viewBox="0 0 512 512" stroke-width="78" stroke-linecap="round">
                        <rect width="512" height="512" rx="115" fill="#fff"/>
                        <path stroke="#36c5f0" d="m110 207h97m0-97h.1v-.1"/>
                        <path stroke="#2eb67d" d="m305 110v97m97 0v.1h.1"/>
                        <path stroke="#ecb22e" d="m402 305h-97m0 97h-.1v.1"/>
                        <path stroke="#e01e5a" d="M110 305h.1v.1m97 0v97"/>
                    </svg>
                </span>
                Join Slack
            </a>
            <a href="https://x.com/eGovernmentOS" target="_blank">
                <span class="icon">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z">
                        </path>
                    </svg>
                </span>
                Twitter
            </a>
        </div>
        <p style="text-align:center; margin-top:1.5rem; color:var(--muted); font-size:0.95rem;">
            Have questions or want to contribute? We’d love to hear from you.
        </p>
    </section>

    <section>
        <div class="section-head"><span class="label"><svg version="1.1" xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" width="32" height="32"
                    style="enable-background:new 0 0 1024 1024;" xml:space="preserve">
                    <style type="text/css">
                        .st0 {
                            fill: none;
                        }

                        .st1 {
                            clip-path: url(#SVGID_3_);
                            fill: none;
                            stroke: #fff;
                            stroke-width: 209;
                            stroke-miterlimit: 10;
                        }

                        .st2 {
                            clip-path: url(#SVGID_5_);
                            fill: none;
                            stroke: #fff;
                            stroke-width: 209;
                            stroke-miterlimit: 10;
                        }
                    </style>
                    <g>
                        <g>
                            <circle id="SVGID_1_" class="st0" cx="513.3" cy="510.8" r="454.9" />
                        </g>
                        <g>
                            <g>
                                <defs>
                                    <circle id="SVGID_2_" cx="513.3" cy="510.8" r="454.9" />
                                </defs>
                                <clipPath id="SVGID_3_">
                                    <use xlink:href="#SVGID_2_" style="overflow:visible;" />
                                </clipPath>
                                <circle class="st1" cx="758.2" cy="988.4" r="411.5" />
                            </g>
                        </g>
                        <g>
                            <g>
                                <defs>
                                    <circle id="SVGID_4_" cx="513.3" cy="510.8" r="454.9" />
                                </defs>
                                <clipPath id="SVGID_5_">
                                    <use xlink:href="#SVGID_4_" style="overflow:visible;" />
                                </clipPath>
                                <circle class="st2" cx="262" cy="81.4" r="411.5" />
                            </g>
                        </g>
                    </g>
                </svg><span class="titanium">eGovernmentOS</span></span></div>
    </section>

    <canvas id="titanium-bg"></canvas>

    <script>
        const canvas = document.getElementById('titanium-bg');
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];

        // Titanium colors palette (metallic greys/silvers)
        const colors = ['#E5E7EB', '#D1D5DB', '#9CA3AF', '#4B5563'];

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }

        class Particle {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.size = Math.random() * 2 + 0.5;
                this.color = colors[Math.floor(Math.random() * colors.length)];
                this.opacity = Math.random() * 0.5 + 0.1;
                this.fadeSpeed = 0.005;
                this.fadingIn = true;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                // Bounce off edges
                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;

                // Shimmer effect (opacity oscillation)
                if (this.fadingIn) {
                    this.opacity += this.fadeSpeed;
                    if (this.opacity >= 0.8) this.fadingIn = false;
                } else {
                    this.opacity -= this.fadeSpeed;
                    if (this.opacity <= 0.1) this.fadingIn = true;
                }
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.opacity;
                ctx.fill();
                ctx.globalAlpha = 1;

                // Shiny glow core
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.color;
                ctx.shadowBlur = 0;
            }
        }

        function init() {
            resize();
            particles = [];
            for (let i = 0; i < 100; i++) {
                particles.push(new Particle());
            }
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);
            
            // Draw gradient background
            const gradient = ctx.createLinearGradient(0, 0, 0, height);
            gradient.addColorStop(0, '#0f172a'); // Dark slate/titanium base
            gradient.addColorStop(1, '#000000');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, width, height);

            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        }

        window.addEventListener('resize', () => {
            resize();
            init();
        });

        init();
        animate();
    </script>
</body>

</html>
  )";
  std::move(callback).Run(
      base::MakeRefCounted<base::RefCountedString>(std::move(source)));
}

class NxtscapeFirstRun;
class NxtscapeFirstRunUIConfig
    : public content::DefaultWebUIConfig<NxtscapeFirstRun> {
public:
  NxtscapeFirstRunUIConfig()
      : DefaultWebUIConfig("chrome", "egovernmentos-first-run") {}
};

class NxtscapeFirstRun : public content::WebUIController {
public:
  NxtscapeFirstRun(content::WebUI *web_ui) : content::WebUIController(web_ui) {
    content::URLDataSource::Add(Profile::FromWebUI(web_ui),
                                std::make_unique<UFRDataSource>());
  }
  NxtscapeFirstRun(const NxtscapeFirstRun &) = delete;
  NxtscapeFirstRun &operator=(const NxtscapeFirstRun &) = delete;
};

#endif // CHROME_BROWSER_UI_WEBUI_NXTSCAPE_FIRST_RUN_H_
