﻿#if ZIP_AVAILABLE

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

using kumaS.NuGetImporter.Editor.DataClasses;

using UnityEditor;

using UnityEngine;

namespace kumaS.NuGetImporter.Editor
{
    /// <summary>
    /// <para>Class that provides extend methods to display the package information as a GUI.</para>
    /// <para>パッケージの情報をGUIとして表示する拡張メソッドを提供するクラス。</para>
    /// </summary>
    public static class PackageDataExtentionToGUI
    {
        private static HttpClient client = new HttpClient();
        private static readonly Dictionary<string, Task> getting = new Dictionary<string, Task>();
        private static readonly Dictionary<string, Texture2D> iconCache = new Dictionary<string, Texture2D>();
        private static readonly List<string> iconLog = new List<string>();

        private static List<Task> timeoutSet = new List<Task>();
        private static Stack<TimeSpan> timeoutStack = new Stack<TimeSpan>();

        /// <summary>
        /// <para>Delete icon cache.</para>
        /// <para>アイコンのキャッシュを削除する。</para>
        /// </summary>
        public static void DeleteCache()
        {
            lock (iconCache)
            {
                iconCache.Clear();
                iconLog.Clear();
                getting.Clear();
            }
        }

        /// <summary>
        /// <para>Set Timeout.</para>
        /// <para>タイムアウト時間を再設定。</para>
        /// </summary>
        /// <param name="timeout"></param>
        /// <returns></returns>
        public static async Task SetTimeout(TimeSpan timeout)
        {
            lock (timeoutStack)
            {
                if (timeoutStack.Any())
                {
                    timeoutStack.Push(timeout);
                    return;
                }
                timeoutStack.Push(timeout);
            }
            var task = SetWebClientTasks();
            timeoutSet.Add(task);
            await task;
            timeoutSet.Clear();
        }

        private static async Task SetWebClientTasks()
        {
            await Task.WhenAll(getting.Values.ToArray());
            client.Dispose();
            client = new HttpClient(new HttpClientHandler() { AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate });
            lock (timeoutStack)
            {
                client.Timeout = timeoutStack.Pop();
                timeoutStack.Clear();
            }
        }

        /// <summary>
        /// <para>Display the package information as a GUI.</para>
        /// <para>パッケージ情報をGUIとして表示する。</para>
        /// </summary>
        /// <param name="data">
        /// <para>Package infomation.</para>
        /// <para>パッケージ情報。</para>
        /// </param>
        /// <param name="bold">
        /// <para>Bold GUIStyle.</para>
        /// <para>太字のGUIStyle。</para>
        /// </param>
        /// <param name="window">
        /// <para>Main window of NuGet importer.</para>
        /// <para>NuGet importerのメインウィンドウ。</para>
        /// </param>
        /// <param name="selected">
        /// <para>Whether the package is selected.</para>
        /// <para>選択されたパッケージかどうか。</para>
        /// </param>
        /// <param name="onlyStable">
        /// <para>Whether only stable.</para>
        /// <para>安定版のみか。</para>
        /// </param>
        /// <returns>
        /// <para>Task</para>
        /// </returns>
        internal static async Task ToGUI(this Datum data, GUIStyle bold, NuGetImporterWindow window, bool selected, bool onlyStable)
        {
            var tasks = new List<Task>();
            var sizeScale = window.position.width / 1920;
            if (onlyStable)
            {
                if (!data.versions.Any(version => !version.version.Contains('-') && version.version[0] != '0'))
                {
                    return;
                }
            }

            Color color = GUI.color;
            if (selected)
            {
                GUI.color = Color.cyan;
            }

            using (var scope = new EditorGUILayout.HorizontalScope("Box", GUILayout.MinHeight(150), GUILayout.ExpandWidth(true)))
            {
                GUI.color = color;
                Event currentEvent = Event.current;
                if (currentEvent.type == EventType.MouseDown)
                {
                    if (scope.rect.Contains(currentEvent.mousePosition))
                    {
                        tasks.Add(window.UpdateSelected(data));
                    }
                }
                using (new EditorGUILayout.VerticalScope(GUILayout.MinHeight(150), GUILayout.Width(150 * sizeScale)))
                {
                    GUILayout.FlexibleSpace();
                    using (new EditorGUILayout.HorizontalScope())
                    {
                        GUILayout.FlexibleSpace();
                        EditorGUILayout.LabelField(new GUIContent(data.icon), GUILayout.Width(128 * sizeScale), GUILayout.Height(128 * sizeScale));
                        GUILayout.FlexibleSpace();
                    }
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.VerticalScope(GUILayout.ExpandWidth(true)))
                {
                    using (new EditorGUILayout.HorizontalScope(GUILayout.ExpandWidth(true)))
                    {
                        GUILayoutExtention.WrapedLabel(data.id, 24);
                    }

                    using (new EditorGUILayout.HorizontalScope(GUILayout.ExpandWidth(true)))
                    {
                        GUILayout.Label("Author : ", bold);
                        GUILayoutExtention.WrapedLabel(string.Join(", ", data.authors));
                        GUILayout.Label("Download :", bold);
                        GUILayout.Label(data.totalDownloads.ToString());
                        GUILayout.FlexibleSpace();
                        IEnumerable<string> sortedVersions = data.GetAllVersion().AsEnumerable().Reverse();
                        var version = onlyStable ? sortedVersions.First(ver => !ver.Contains('-') && ver[0] != '0') : sortedVersions.First();
                        if (PackageManager.Installed != null && PackageManager.Installed.package != null)
                        {
                            IEnumerable<Package> installed = PackageManager.Installed.package.Where(package => package.id == data.id);
                            if (installed != null && installed.Any())
                            {
                                version = installed.First().version;
                            }
                        }
                        GUILayout.Label("v" + version);
                    }
                    GUILayoutExtention.WrapedLabel(data.summary == "" ? data.description : data.summary);
                }
            }

            await Task.WhenAll(tasks);
        }

        /// <summary>
        /// <para>Get the icon for this package.</para>
        /// <para>このパッケージのアイコンを取得する。</para>
        /// </summary>
        /// <param name="data">
        /// <para>Package infomation.</para>
        /// <para>パッケージ情報。</para>
        /// </param>
        /// <returns>
        /// <para>Task</para>
        /// </returns>
        public static async Task GetIcon(this Datum data)
        {
            if (data.iconUrl == null || data.iconUrl == "")
            {
                data.icon = null;
                return;
            }

            // The below code is the cache process.
            lock (iconCache)
            {
                var haveIcon = iconCache.ContainsKey(data.iconUrl);
                if (haveIcon)
                {
                    iconLog.Remove(data.iconUrl);
                    iconLog.Add(data.iconUrl);
                    data.icon = iconCache[data.iconUrl];
                    return;
                }
            }

            var isGetting = false;
            lock (getting)
            {
                isGetting = getting.ContainsKey(data.iconUrl);
            }

            var isSavemode = NuGetImporterSettings.Instance.IsNetworkSavemode;
            if (isSavemode)
            {
                data.icon = null;
                return;
            }

            if (!isGetting)
            {
                lock (getting)
                {
                    getting.Add(data.iconUrl, GetIcon(data.iconUrl));
                }
            }

            await getting[data.iconUrl];
            lock (getting)
            {
                getting.Remove(data.iconUrl);
            }

            data.icon = iconCache[data.iconUrl];
        }

        /// <summary>
        /// <para>Display the package information as a GUI.</para>
        /// <para>パッケージ情報をGUIとして表示する。</para>
        /// </summary>
        /// <param name="data">
        /// <para>Package infomation.</para>
        /// <para>パッケージ情報。</para>
        /// </param>
        /// <param name="bold">
        /// <para>Bold GUIStyle.</para>
        /// <para>太字のGUIStyle。</para>
        /// </param>
        /// <param name="window">
        /// <para>Main window of NuGet importer.</para>
        /// <para>NuGet importerのメインウィンドウ。</para>
        /// </param>
        /// <param name="selected">
        /// <para>Whether the package is selected.</para>
        /// <para>選択されたパッケージかどうか。</para>
        /// </param>
        /// <param name="installedVersion">
        /// <para>Installed version.</para>
        /// <para>インストールされているバージョン。</para>
        /// </param>
        internal static void ToGUI(this Catalog data, GUIStyle bold, NuGetImporterWindow window, bool selected, string installedVersion)
        {
            var sizeScale = window.position.width / 1920;
            Color color = GUI.color;
            if (selected)
            {
                GUI.color = Color.cyan;
            }
            Catalogentry catalogEntry = data.GetAllCatalogEntry().Where(catalog => catalog.version == installedVersion).First();
            using (var scope = new EditorGUILayout.HorizontalScope("Box", GUILayout.MinHeight(150), GUILayout.ExpandWidth(true)))
            {
                GUI.color = color;
                Event currentEvent = Event.current;
                if (currentEvent.type == EventType.MouseDown)
                {
                    if (scope.rect.Contains(currentEvent.mousePosition))
                    {
                        window.UpdateSelected(data);
                    }
                }
                using (new EditorGUILayout.VerticalScope(GUILayout.MinHeight(150), GUILayout.Width(150 * sizeScale)))
                {
                    GUILayout.FlexibleSpace();
                    using (new EditorGUILayout.HorizontalScope())
                    {
                        GUILayout.FlexibleSpace();
                        EditorGUILayout.LabelField(new GUIContent(data.icon), GUILayout.Width(128 * sizeScale), GUILayout.Height(128 * sizeScale));
                        GUILayout.FlexibleSpace();
                    }
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.VerticalScope(GUILayout.ExpandWidth(true)))
                {
                    using (new EditorGUILayout.HorizontalScope(GUILayout.ExpandWidth(true)))
                    {
                        GUILayoutExtention.WrapedLabel(catalogEntry.id, 24);
                    }
                    using (new EditorGUILayout.HorizontalScope(GUILayout.ExpandWidth(true)))
                    {
                        GUILayout.Label("Author : ", bold);
                        GUILayout.Label(string.Join(", ", catalogEntry.authors));
                        GUILayout.FlexibleSpace();
                        GUILayout.Label("v" + installedVersion);
                    }
                    GUILayoutExtention.WrapedLabel(catalogEntry.summary == "" ? catalogEntry.description : catalogEntry.summary);
                }
            }
        }

        /// <summary>
        /// <para>Display the package information details as a GUI.</para>
        /// <para>パッケージ情報の詳細をGUIとして表示する。</para>
        /// </summary>
        /// <param name="data">
        /// <para>Package infomation.</para>
        /// <para>パッケージ情報。</para>
        /// </param>
        /// <param name="bold">
        /// <para>Bold GUIStyle.</para>
        /// <para>太字のGUIStyle。</para>
        /// </param>
        /// <param name="selectedVersion">
        /// <para>Selected version.</para>
        /// <para>選択されているバージョン。</para>
        /// </param>
        internal static void ToDetailGUI(this Catalog data, GUIStyle bold, string selectedVersion)
        {
            IEnumerable<Catalogentry> catalogEntrys = data.GetAllCatalogEntry().Where(catalog => catalog.version == selectedVersion);
            if (!catalogEntrys.Any())
            {
                return;
            }
            Catalogentry catalogEntry = catalogEntrys.First();

            using (new EditorGUILayout.VerticalScope("Box"))
            {
                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("Description", bold);
                }

                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayoutExtention.WrapedLabel(catalogEntry.description == "" ? catalogEntry.summary : catalogEntry.description);
                }
            }

            using (new EditorGUILayout.VerticalScope("Box"))
            {
                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("Version : ", bold);
                    GUILayoutExtention.WrapedLabel(selectedVersion);
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("Auther :", bold);
                    GUILayoutExtention.WrapedLabel(string.Join(", ", catalogEntry.authors));
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("License : ", bold);
                    GUILayoutExtention.UrlLabel(catalogEntry.licenseExpression == "" ? catalogEntry.licenseUrl : catalogEntry.licenseExpression, catalogEntry.licenseUrl);
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("Publish date : ", bold);
                    GUILayoutExtention.WrapedLabel(catalogEntry.published);
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("Project url : ", bold);
                    GUILayoutExtention.UrlLabel(catalogEntry.projectUrl, catalogEntry.projectUrl);
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.HorizontalScope())
                {
                    GUILayout.Label("Tag : ", bold);
                    GUILayoutExtention.WrapedLabel(string.Join(", ", catalogEntry.tags));
                    GUILayout.FlexibleSpace();
                }
            }

            using (new EditorGUILayout.VerticalScope("Box"))
            {
                GUILayout.Label("Dependency", bold);

                if (catalogEntry.dependencyGroups == null)
                {
                    GUILayout.Label("    None");
                }
                else
                {
                    List<string> framework = FrameworkName.TARGET;

                    IEnumerable<Dependencygroup> dependencyGroups = catalogEntry.dependencyGroups.Where(group => group.targetFramework == null || group.targetFramework == "" || framework.Contains(group.targetFramework));
                    if (dependencyGroups == null || !dependencyGroups.Any())
                    {
                        GUILayout.Label("    None");
                    }
                    else
                    {
                        var dependencies = new List<Dependency>();
                        var targetFramework = framework.First();
                        IEnumerable<Dependencygroup> dependAllGroup = dependencyGroups.Where(depend => depend.targetFramework == null || depend.targetFramework == "");
                        if (dependAllGroup.Any())
                        {
                            dependencies.AddRange(dependAllGroup.First().dependencies);
                        }

                        IOrderedEnumerable<Dependencygroup> dependGroups = dependencyGroups.Except(dependAllGroup).OrderBy(group =>
                        {
                            var ret = framework.IndexOf(group.targetFramework);
                            return ret < 0 ? int.MaxValue : ret;
                        });

                        if (dependGroups.Any() && dependGroups.First().dependencies != null)
                        {
                            Dependencygroup dependGroup = dependGroups.First();
                            dependencies.AddRange(dependGroup.dependencies);
                            if (dependGroup.dependencies.Any())
                            {
                                targetFramework = dependGroup.targetFramework;
                            }
                        }

                        GUILayout.Label("    " + targetFramework, bold);
                        if (!dependencies.Any())
                        {
                            GUILayout.Label("        None");
                        }
                        else
                        {
                            try
                            {
                                foreach (Dependency dependency in dependencies)
                                {
                                    GUILayout.Label("        " + dependency.id + "  (" + SemVer.ToMathExpression(dependency.range) + ")");
                                }
                            }
                            catch (Exception)
                            {
                                // During execution, the number of dependencies changes and an exception occurs, so I grip it. (because it's not a problem.)
                            }
                        }
                    }
                }

            }

            GUILayout.FlexibleSpace();
        }

        /// <summary>
        /// <para>Displays an overview of the package information as a GUI.</para>
        /// <para>パッケージの概要をGUIとして表示する。</para>
        /// </summary>
        /// <param name="summary">
        /// <para>An overview of the package information.</para>
        /// <para>パッケージの概要。</para>
        /// </param>
        /// <param name="bold">
        /// <para>Bold GUIStyle.</para>
        /// <para>太字のGUIStyle。</para>
        /// </param>
        /// <param name="window">
        /// <para>Main window of NuGet importer.</para>
        /// <para>NuGet importerのメインウィンドウ。</para>
        /// </param>
        /// <param name="onlyStable">
        /// <para>Whether only stable.</para>
        /// <para>安定版のみか。</para>
        /// </param>
        /// <param name="method">
        /// <para>Method to select a version.</para>
        /// <para>バージョンを選択する方法。</para>
        /// <returns>
        /// <para>Task</para>
        /// </returns>
        internal static async Task ToGUI(this PackageSummary summary, GUIStyle bold, NuGetImporterWindow window, bool isReady, bool onlyStable, VersionSelectMethod method)
        {
            var tasks = new List<Task>();
            var sizeScale = window.position.width / 1920;
            var isExist = PackageManager.ExiestingPackage.package.Any(package => package.id == summary.PackageId);
            using (new EditorGUILayout.HorizontalScope(GUILayout.Height(150)))
            {
                using (new EditorGUILayout.VerticalScope(GUILayout.Width(150 * sizeScale)))
                {
                    GUILayout.FlexibleSpace();
                    using (new EditorGUILayout.HorizontalScope())
                    {
                        GUILayout.FlexibleSpace();
                        EditorGUILayout.LabelField(new GUIContent(summary.Image), GUILayout.Width(128 * sizeScale), GUILayout.Height(128 * sizeScale));
                        GUILayout.FlexibleSpace();
                    }
                    GUILayout.FlexibleSpace();
                }

                using (new EditorGUILayout.VerticalScope(GUILayout.ExpandWidth(true)))
                {
                    using (new EditorGUILayout.HorizontalScope())
                    {
                        GUILayoutExtention.WrapedLabel(summary.PackageId, 24);
                    }

                    using (new EditorGUILayout.HorizontalScope())
                    {
                        GUILayout.Label("version", bold);
                        List<string> versions = onlyStable ? summary.StableVersion : summary.AllVersion;
                        var index = versions.Contains(summary.SelectedVersion) ? versions.IndexOf(summary.SelectedVersion) : 0;
                        summary.SelectedVersion = versions[EditorGUILayout.Popup(index, versions.ToArray(), GUILayout.ExpandWidth(true))];
                        var isSameVersion = summary.SelectedVersion == summary.InstalledVersion;
                        var installText = summary.InstalledVersion == null ? "Install" : isSameVersion ? "Repair" : "Change Version";
                        using (new EditorGUI.DisabledGroupScope(!isReady || isExist))
                        {
                            if (GUILayout.Button(installText, GUILayout.ExpandWidth(true)))
                            {
                                if (summary.InstalledVersion == null)
                                {
                                    tasks.Add(PackageOperation(PackageManager.InstallPackageAsync(summary.PackageId, summary.SelectedVersion, onlyStable, method), window, summary.PackageId));
                                }
                                else if (isSameVersion)
                                {
                                    tasks.Add(PackageOperation(PackageManager.FixPackageAsync(summary.PackageId, false), window, summary.PackageId));
                                }
                                else
                                {
                                    tasks.Add(PackageOperation(PackageManager.ChangePackageVersionAsync(summary.PackageId, summary.SelectedVersion, onlyStable, method), window, summary.PackageId));
                                }
                            }

                            using (new EditorGUI.DisabledScope(!isSameVersion))
                            {
                                if (GUILayout.Button("Uninstall", GUILayout.ExpandWidth(true)))
                                {
                                    tasks.Add(PackageOperation(PackageManager.UninstallPackagesAsync(summary.PackageId, onlyStable), window, summary.PackageId));
                                }
                            }
                        }
                    }

                    if (isExist)
                    {
                        using (new EditorGUILayout.HorizontalScope())
                        {
                            GUILayout.Label("This package exists out of control in this project.");
                        }
                    }
                }
            }
            await Task.WhenAll(tasks);
        }

        private static async Task PackageOperation(Task<OperationResult> operation, NuGetImporterWindow window, string packageId)
        {
            OperationResult result = await operation;
            EditorUtility.DisplayDialog("NuGet  importer", result.Message, "OK");
            await window.UpdateInstalledList();
            await window.UpdateSelected(packageId);
        }

        /// <summary>
        /// <para>Get the icon for this package.</para>
        /// <para>このパッケージのアイコンを取得する。</para>
        /// </summary>
        /// <param name="data">
        /// <para>Package infomation.</para>
        /// <para>パッケージ情報。</para>
        /// </param>
        /// <returns>
        /// <para>Task</para>
        /// </returns>
        public static async Task GetIcon(this Catalog data, string installedVersion)
        {
            Catalogentry d = data.GetAllCatalogEntry().First(catalog => catalog.version == installedVersion);

            if (d.iconUrl == null || d.iconUrl == "")
            {
                data.icon = null;
                return;
            }

            // The below code is the cache process.
            lock (iconCache)
            {
                var haveIcon = iconCache.ContainsKey(d.iconUrl);
                if (haveIcon)
                {
                    iconLog.Remove(d.iconUrl);
                    iconLog.Add(d.iconUrl);
                    data.icon = iconCache[d.iconUrl];
                    return;
                }
            }

            var isGetting = false;
            lock (getting)
            {
                isGetting = getting.ContainsKey(d.iconUrl);
            }
            if (!isGetting)
            {
                if (timeoutSet.Any())
                {
                    await Task.WhenAll(timeoutSet.ToArray());
                }

                lock (getting)
                {
                    getting.Add(d.iconUrl, GetIcon(d.iconUrl));
                }
            }

            await getting[d.iconUrl];
            lock (getting)
            {
                getting.Remove(d.iconUrl);
            }

            data.icon = iconCache[d.iconUrl];
        }


        private static async Task GetIcon(string url)
        {
            var source = new Texture2D(0, 0, TextureFormat.RGBA32, false);
            var tryCount = NuGetImporterSettings.Instance.RetryLimit + 1;
            for (var i = 0; i < tryCount; i++)
            {
                try
                {
                    var data = await client.GetByteArrayAsync(url);
                    source.LoadImage(data);
                    break;
                }
                catch (Exception e)
                {
                    if (e.Message == "404 (Not Found)")
                    {
                        UpdateIconCache(url, null);
                        break;
                    }
                    if (i >= tryCount - 1)
                    {
                        lock (getting)
                        {
                            getting.Clear();
                        }
                        throw;
                    }
                    await Task.Delay(1000);
                }
            }
            var texture = new Texture2D(128, 128, TextureFormat.RGBA32, false);
            Graphics.ConvertTexture(source, texture);
            MonoBehaviour.DestroyImmediate(source);
            UpdateIconCache(url, texture);
        }

        private static void UpdateIconCache(string url, Texture2D texture)
        {
            lock (iconCache)
            {
                iconCache[url] = texture;
                iconLog.Add(url);
                while (iconCache.Count > NuGetImporterSettings.Instance.IconCacheLimit && iconCache.Count > 0)
                {
                    var delete = iconLog[0];
                    iconLog.RemoveAt(0);
                    MonoBehaviour.DestroyImmediate(iconCache[delete]);
                    iconCache.Remove(delete);
                }
            }
        }
    }
}

#endif